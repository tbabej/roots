from zipfile import ZipFile

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import redirect, render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from base.util import convert_files_to_single_pdf, get_uploaded_filepath

from problems.models import Problem, UserSolution
from problems.forms import UserSolutionForm, ImportCorrectedSolutionsForm


class ProblemListView(ListView):

    model = Problem
    context_object_name = 'problems'


class ProblemDetailView(DetailView):

    model = Problem
    context_object_name = 'problem'


class UserSolutionSubmissionView(View):

    form_class = UserSolutionForm

    def get(self, request, *args, **kwargs):
        return redirect('competitions_season_detail_latest')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            data = dict(
                user=request.user,
                problem=Problem.objects.get(pk=form.cleaned_data['problem'])
            )

            submission, created = UserSolution.objects.get_or_create(**data)

            try:
                filelist = request.FILES.getlist('solution')
                submission.solution = convert_files_to_single_pdf(
                                          submission.get_solution_path(),
                                          filelist)
                submission.save()
            except ValidationError, e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.iteritems():
                messages.error(request, u"{error}".format(
                                    error=', '.join(errors))
                              )

        return redirect('competitions_season_detail_latest')


# TODO: make this view protected so that only staff members can use it
# TODO: make sure this gets proper treatement when row-level permissions are
#       introduced
class ImportCorrectedSolutionsView(View):

    form_class = ImportCorrectedSolutionsForm

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/import_corrected_solutions.html',
                      {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            try:
                file_data = form.cleaned_data['zipfile']
                filepath = get_uploaded_filepath(file_data)
                solutions_zip = ZipFile(filepath)

                # Check for any corrupted files in the zip
                # testzip returns the list of corrupted ones
                if solutions_zip.testzip():
                    messages.error(request,
                                   '"%s" in the .zip archive is corrupt.'
                                   % solutions_zip.testzip())
                    raise Exception('Corrpted archive.')

                # We loop over all PDF files in the zip
                for filename in [name for name in solutions_zip.namelist()
                                 if name.endswith('.pdf')]:

                    # Check that the name is of the form
                    # <score>-<username>-<problem_pk>.pdf
                    try:
                        parts = filename.rstrip('.pdf').split('-')

                        score = int(parts[0])
                        username = '-'.join(parts[1:-1])
                        problem_pk = int(parts[-1])

                    except (IndexError, ValueError, AssertionError):
                        messages.error(request,
                                       '"%s" is not of the correct form '
                                       '<score>-<username>-<problem_pk>.pdf')
                        continue

                    # Find the UserSolution and modify it
                    try:
                        user = User.objects.get(username=username)
                        solution = UserSolution.objects.get(user=user,
                                                            problem=problem_pk)
                    except User.DoesNotExist:
                        messages.error('User %s does not exist' % username)
                        continue
                    except UserSolution.DoesNotExist:
                        messages.error(request,
                                       'Solution for user %s and problem '
                                       '%d does not exist.'
                                       % (username, problem_pk))
                        continue

                    solution.score = score
                    solution.save()

            except Exception, e:
                # If any exceptions happened, errors should be in messages
                messages.error(request, 'exception happened: %s' % e)
            finally:
                # redirect back to admin site
                return redirect('admin:problems_usersolution_changelist')

        else:
            return render(request, 'admin/import_corrected_solutions.html',
                          {'form': form})
