//document.addEventListener('DOMContentLoaded', function() {
//    const htmlCodeTextarea = document.getElementById('html-code');
//    const previewFrame = document.getElementById('preview-frame');
//
//    // 更新 iframe 内容的函数
//    function updatePreview() {
//        const htmlCode = htmlCodeTextarea.value;
//        const iframeDoc = previewFrame.contentDocument || previewFrame.contentWindow.document;
//        iframeDoc.open();
//        iframeDoc.write(htmlCode);
//        iframeDoc.close();
//    }
//
//    // 监听 textarea 的输入变化，实时更新预览
//    htmlCodeTextarea.addEventListener('input', updatePreview);
//
//    // 初次加载时更新预览
//    updatePreview();
//});

document.addEventListener('DOMContentLoaded', function() {
    const htmlCodeTextarea = document.getElementById('html-code');
    const previewFrame = document.getElementById('preview-frame');

    // update iframe
    function updatePreview() {
        const htmlCode = htmlCodeTextarea.value;
        previewFrame.srcdoc = htmlCode;
    }

    htmlCodeTextarea.addEventListener('input', updatePreview);

    updatePreview();
});
