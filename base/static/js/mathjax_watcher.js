// select the target node
var target = document.querySelector("[id^='comments']");

// create an observer instance
var observer = new MutationObserver(function(mutations) {
  MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
});

// configuration of the observer:
var config = { attributes: true, childList: true, subtree: true };

// pass in the target node, as well as the observer options
observer.observe(target, config);
