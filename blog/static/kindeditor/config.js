KindEditor.ready(function(K) {
    K.create('#id_content', {
        width:'800px',
        height:'200px',
        formatUploadUrl: false,
        uploadJson: '/admin/upload/kindeditor'
    });
});