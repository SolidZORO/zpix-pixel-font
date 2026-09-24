var showLoadingEl = document.getElementById('show-loading');
var showCharactersEl = document.getElementById('show-characters');

// Two-way binding between the textarea and ?text=:
// - on load, ?text= fills the textarea (a literal "\n" also becomes a break)
// - on input, the textarea syncs back to ?text= (replaceState, no reload)
(function bindTextParam() {
  var input = document.querySelector('.input-characters');
  if (!input) return;

  var params = new URLSearchParams(window.location.search);
  if (params.has('text')) {
    input.value = params.get('text').replace(/\\n/g, '\n');
  }

  if (!window.history || !window.history.replaceState) return;
  var timer = null;
  input.addEventListener('input', function () {
    if (timer) clearTimeout(timer);
    timer = setTimeout(function () {
      var url = new URL(window.location.href);
      if (input.value) url.searchParams.set('text', input.value);
      else url.searchParams.delete('text');
      window.history.replaceState(null, '', url.toString());
    }, 300);
  });

  input.dispatchEvent(new Event('input', { bubbles: true }));
})();

document.fonts.ready.then(function() {
  // console.log('All fonts in use by visible text have loaded.');
  showLoadingEl.classList.add('hide');
  showCharactersEl.classList.add('show');
});
