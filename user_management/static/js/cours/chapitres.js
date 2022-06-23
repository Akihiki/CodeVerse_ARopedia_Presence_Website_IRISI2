$(function(){                                    
    $('.chapitre-search-by').change(function () {
        let url = $(this).val();
        if (url) {
            window.location = url;
        }
    });
});
