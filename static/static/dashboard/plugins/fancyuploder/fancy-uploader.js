$(function() {
    //fancyfileuplod
    $('#img-file').FancyFileUpload({
        params: {
            action: 'fileuploader'
        },
        maxfilesize: 1000000
    });
});