// title
var hiddenProperty = 'hidden' in document ? 'hidden' :
    'webkitHidden' in document ? 'webkitHidden' :
        'mozHidden' in document ? 'mozHidden' : null;
var title = document.querySelector('title');
var visibilityChangeEvent = hiddenProperty.replace(/hidden/i, 'visibilitychange');
var onVisibilityChange = function () {
    if (!document[hiddenProperty]) {
        title.innerHTML = 'ヾ(^▽^*)))回来啦💖';
        setTimeout(() => {
            title.innerHTML = '(´▽`ʃ♡ƪ)爱你哟❤';
        }, 2000)
    } else {
        title.innerHTML = '(ToT)/~~你不爱我了💔';
    }
}
document.addEventListener(visibilityChangeEvent, onVisibilityChange);
