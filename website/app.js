var showLoadingEl = document.getElementById('show-loading');
var showCharactersEl = document.getElementById('show-characters');

document.fonts.ready.then(function() {
  // console.log('All fonts in use by visible text have loaded.');
  showLoadingEl.classList.add('hide');
  showCharactersEl.classList.add('show');
});
