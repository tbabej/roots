from photologue.views import GalleryArchiveIndexView


class GallerySampleArchiveIndexView(GalleryArchiveIndexView):
    template_name = "photologue/gallery_archive.html"

    def get_context_data(self, **kwargs):
        context = super(GallerySampleArchiveIndexView, self)\
                      .get_context_data(**kwargs)

        extended_latest = []

        if 'latest' not in context:
            return context

        for gallery in context['latest']:
            sample = gallery.sample(count=4)
            all_photos = gallery.public().order_by('date_added', 'pk')

            extended_latest.append((gallery, all_photos, sample))

        context['extended_latest'] = extended_latest
        return context