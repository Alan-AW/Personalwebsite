$(document).ready(function () {
    $(".animsition").animsition({
        inClass: 'fade-in-up',  // 进入页面时的动画属性
        outClass: 'fade-out-down',  // 离开页面时的动画属性
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        // e.g. linkElement: 'a:not([target="_blank"]):not([href^="#"])'
        loading: true,
        loadingParentElement: 'body', //animsition wrapper element
        loadingClass: 'animsition-loading',
        loadingInner: '', // e.g '<img src="loading.svg" />'
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: ['animation-duration', '-webkit-animation-duration'],
        // "browser" option allows you to disable the "animsition" in case the css property in the array is not supported by your browser.
        // The default setting is to disable the "animsition" in a browser that does not support "animation-duration".
        overlay: false,
        overlayClass: 'animsition-overlay-slide',
        overlayParentElement: 'body',
        transition: function (url) {
            window.location.href = url;
        }
    });
});

/*
关于inclass和outclass
进入页面和离开页面显示的效果主要靠这两个属性控制
一共有58种样式：
 Fade
fade-in	fade-out
 Fade up
fade-in-up-sm	    fade-in-up	        fade-in-up-lg	        fade-out-up-sm	    fade-out-up	    fade-out-up-lg
 Fade down
fade-in-down-sm	    fade-in-down	    fade-in-down-lg	        fade-out-down-sm	fade-out-down	fade-out-down-lg
 Fade left
fade-in-left-sm	    fade-in-left	    fade-in-left-lg	        fade-out-left-sm	fade-out-left	fade-out-left-lg
 Fade right
fade-in-right-sm	fade-in-right	    fade-in-right-lg	    fade-out-right-sm	fade-out-right	fade-out-right-lg
 Rotate
rotate-in-sm	    rotate-in	        rotate-in-lg	        rotate-out-sm	    rotate-out	    rotate-out-lg
 Flip X
flip-in-x-fr	    flip-in-x	        flip-in-x-nr	        flip-out-x-fr	    flip-out-x	    flip-out-x-nr
 Flip Y
flip-in-y-fr	    flip-in-y	        flip-in-y-nr	        flip-out-fr	        flip-out-y	    flip-out-y-nr
 Zoom
zoom-in-sm	        zoom-in	zoom-in-lg	zoom-out-sm	zoom-out	zoom-out-lg
*/