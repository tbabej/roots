import os
import zipfile
import StringIO

from django.http import HttpResponse

from competitions.models import Competition


class PrettyFilterMixin(object):

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"


class RestrictedCompetitionAdminMixin(object):
    """
    Extends ModelAdmin in the following ways:
        - makes visible only those objects whose competition_field is one of
          the competitions that request.user organizes
        - makes it possible for the user to assign objects to those competitions
          that he organizes

    Following class attributes can be set to modify the behaviour of this mixin:
        - competition_field: Specifies the field that contains the foreign key
                             to the competition that this object belongs to.
                             Note that this can span several objects through
                             foreign keys, that is, it does not need to be
                             a attribute directly on this model.
    """

    competition_field = 'competition'

    def get_queryset(self, request):
        qs = super(RestrictedCompetitionAdminMixin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        # TODO: Investigate adding querysets, for now exclude all objects
        #       associated with the competitions user does not organize

        competitions = [c.id for c
                        in request.user.userprofile.organized_competitions]
        not_organized_competitions = Competition.objects.exclude(
                                                           id__in=competitions)
        kwargs = {self.competition_field + '__in': not_organized_competitions}
        return qs.exclude(**kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:
            if db_field.name == self.competition_field:
                profile = request.user.userprofile
                kwargs["queryset"] = profile.organized_competitions

        return super(RestrictedCompetitionAdminMixin,
                     self).formfield_for_foreignkey(db_field, request, **kwargs)


class MediaRemovalAdminMixin(object):
    """
    This mixin overrides default delete_selected Admin action and replaces it
    with one that actually constructs a model instance from each object in the
    queryset and calls .delete() upon that instance.

    This way, we ensure that overridden delete method by MediaRemovalMixin
    is called.
    """

    def get_actions(self, request):
        actions = super(MediaRemovalAdminMixin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        # Add new delete method only for the superuser, as it is quite dangerous
        if request.user.is_superuser:

            # We use self.__class__ here so that self is not binded, otherwise
            # we would be passing 4 arguments instead of 3 (and self twice)
            new_delete = (self.__class__.delete_selected_with_media,
                          "delete_selected_with_media",
                          "Delete objects with associated media files")

            actions['delete_selected_with_media'] = new_delete

        return actions

    def delete_selected_with_media(self, request, queryset):
        for obj in queryset.all():
            obj.delete()


class DownloadMediaFilesMixin(object):

    def get_actions(self, request):
        actions = super(DownloadMediaFilesMixin, self).get_actions(request)

        # We use self.__class__ here so that self is not binded, otherwise
        # we would be passing 4 arguments instead of 3 (and self twice)
        export = (self.__class__.download_media_files,
                  "download_media_files",
                  "Download associated media files")

        actions['download_media_files'] = export
        return actions

    def download_media_files(self, request, queryset):
        export_file = 'export.zip'

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for obj in queryset.all():
            for filepath in obj.get_media_files():
                filepath = os.path.join(obj.media_root, filepath)

                if os.path.exists(filepath):
                    fdir, fname = os.path.split(filepath)
                    zf.write(filepath, fname)
                else:
                    self.message_user(request, '%s has no file saved at %s' %
                                                (obj, filepath))

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        response = HttpResponse(s.getvalue(),
                                mimetype="application/x-zip-compressed")
        # ..and correct content-disposition
        response['Content-Disposition'] = (
            'attachment; filename=%s' % export_file
            )

        return response

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin import helpers, ListFilter
from django.contrib import messages
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.translation import ungettext
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text

csrf_protect_m = method_decorator(csrf_protect)


class ImprovedFilteringVersionAdminMixin(object):
    """
    This class overrides default Django's changelist_view. It should be in the
    top of the inheritance hierarchy, above any class/mixin overriding
    the changelist_view.
    """

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        The 'change list' admin view for this model.
        """
        # Additions by the VersionAdmin
        opts = self.model._meta
        recoverlist_view_name = "%s:%s_%s_recoverlist" % (self.admin_site.name, opts.app_label, opts.module_name)
        addurl_view_name = "%s:%s_%s_add" % (self.admin_site.name, opts.app_label, opts.module_name)
        context = {
            "recoverlist_url": reverse(recoverlist_view_name),
            "add_url": reverse(addurl_view_name),
        }
        context.update(extra_context or {})

        # Original Django code
        from django.contrib.admin.views.main import ERROR_FLAG
        app_label = opts.app_label
        if not self.has_change_permission(request, None):
            raise PermissionDenied

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)

        # Check actions to see if any are available on this changelist
        actions = self.get_actions(request)
        if actions:
            # Add the action checkboxes if there are any actions available.
            list_display = ['action_checkbox'] + list(list_display)

        ChangeList = self.get_changelist(request)
        try:
            self.cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self)
        except IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given
            # and the 'invalid=1' parameter was already in the query string,
            # something is screwed up with the database, so display an error
            # page.
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        # If the request was POSTed, this might be a bulk action or a bulk
        # edit. Try to look up an action or confirmation first, but if this
        # isn't an action the POST will fall through to the bulk edit check,
        # below.
        action_failed = False
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        # Actions with no confirmation
        if (actions and request.method == 'POST' and
                'index' in request.POST and '_save' not in request.POST):
            if selected:
                response = self.response_action(request, queryset=self.cl.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True
            else:
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.message_user(request, msg, messages.WARNING)
                action_failed = True

        # Actions with confirmation
        if (actions and request.method == 'POST' and
                helpers.ACTION_CHECKBOX_NAME in request.POST and
                'index' not in request.POST and '_save' not in request.POST):
            if selected:
                response = self.response_action(request, queryset=self.cl.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True

        # If we're allowing changelist editing, we need to construct a formset
        # for the changelist given all the fields to be edited. Then we'll
        # use the formset to validate/process POSTed data.
        formset = self.cl.formset = None

        # Handle POSTed bulk-edit data.
        if (request.method == "POST" and self.cl.list_editable and
                '_save' in request.POST and not action_failed):
            FormSet = self.get_changelist_formset(request)
            formset = self.cl.formset = FormSet(request.POST, request.FILES, queryset=self.cl.result_list)
            if formset.is_valid():
                changecount = 0
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        self.save_model(request, obj, form, change=True)
                        self.save_related(request, form, formsets=[], change=True)
                        change_msg = self.construct_change_message(request, form, None)
                        self.log_change(request, obj, change_msg)
                        changecount += 1

                if changecount:
                    if changecount == 1:
                        name = force_text(opts.verbose_name)
                    else:
                        name = force_text(opts.verbose_name_plural)
                    msg = ungettext("%(count)s %(name)s was changed successfully.",
                                    "%(count)s %(name)s were changed successfully.",
                                    changecount) % {'count': changecount,
                                                    'name': name,
                                                    'obj': force_text(obj)}
                    self.message_user(request, msg, messages.SUCCESS)

                return HttpResponseRedirect(request.get_full_path())

        # Handle GET -- construct a formset for display.
        elif self.cl.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = self.cl.formset = FormSet(queryset=self.cl.result_list)

        # Build the list of media to be used by the formset.
        if formset:
            media = self.media + formset.media
        else:
            media = self.media

        # Build the action form and populate it with available actions.
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
        else:
            action_form = None

        selection_note_all = ungettext('%(total_count)s selected',
            'All %(total_count)s selected', self.cl.result_count)

        context = {
            'module_name': force_text(opts.verbose_name_plural),
            'selection_note': _('0 of %(cnt)s selected') % {'cnt': len(self.cl.result_list)},
            'selection_note_all': selection_note_all % {'total_count': self.cl.result_count},
            'title': self.cl.title,
            'is_popup': self.cl.is_popup,
            'cl': self.cl,
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'opts': self.cl.opts,
            'app_label': app_label,
            'action_form': action_form,
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
            'actions_selection_counter': self.actions_selection_counter,
            'preserved_filters': self.get_preserved_filters(request),
        }
        context.update(extra_context or {})

        return TemplateResponse(request, self.change_list_template or [
            'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
            'admin/%s/change_list.html' % app_label,
            'admin/change_list.html'
        ], context, current_app=self.admin_site.name)


from django.core.exceptions import ImproperlyConfigured


class LazySimpleListFilter(ListFilter):
    # The parameter that should be used in the query string for that filter.
    parameter_name = None

    def __init__(self, request, params, model, model_admin):
        super(LazySimpleListFilter, self).__init__(
            request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)
        self.request = request
        self.model_admin = model_admin
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    @property
    def lookup_choices(self):
        return list(self.lookups(self.request, self.model_admin) or ())

    def has_output(self):
        return True
        # return len(self.lookup_choices) > 0

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, None)

    def lookups(self, request, model_admin):
        """
        Must be overriden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, cl):
        yield {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('All'),
            }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': cl.get_query_string({
                     self.parameter_name: lookup,
                     }, []),
                'display': title,
                }

class ForeignFieldFilter(LazySimpleListFilter):
    field = None
    sort_lookups = None

    def lookups(self, request, model_admin):
        lookup_values = []

        queryset = model_admin.cl.get_queryset(request)
        field_ids = queryset.values_list(self.field, flat=True)

        foreign_model = model_admin.opts.get_field(self.field).rel.to
        for field_value in foreign_model.objects.filter(id__in=field_ids):
            lookup_values.append((field_value.pk, field_value))

        # Sort the looked up values if sort function was specified
        if self.sort_lookups:
            lookup_values.sort(key=self.sort_lookups)

        return lookup_values

    def queryset(self, request, queryset):
        value = self.value()

        # Check that any value was passed, if not, return unmodified queryset
        if not value:
            return queryset

        # Filter the queryset
        return queryset.filter(**{'{0}__pk'.format(self.field): int(value)})


def foreign_field_filter_factory(field, title=None, sort=None):
    title = title or (field[:1].upper() + field[1:])
    return type(
        "ForeignFieldFilter_{0}".format(field),
        (ForeignFieldFilter,),
        {
            'field': field,
            'title': title,
            'parameter_name': field,
            'sort_lookups': sort,
            }
    )
