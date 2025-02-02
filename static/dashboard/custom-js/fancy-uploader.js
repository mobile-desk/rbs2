$(function() {
    //fancyfileuplod
    $('#img_file').FancyFileUpload({
        url: 'http://127.0.0.1:8000/cms/upload/files',
        params: {
            _token: $('input[name="_token"]').val(),
        },
        maxfilesize: 5000000,

    });
});