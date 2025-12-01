// Small site-wide attendance helpers (declarative).
// Avoids external libs, lightweight.
document.addEventListener('DOMContentLoaded', function(){
  // custom: stop duplicate form submissions
  const forms = document.querySelectorAll('form');
  forms.forEach(f => {
    f.addEventListener('submit', function(ev){
      const btn = f.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.dataset.orig = btn.innerHTML;
        btn.innerHTML = 'Saving...';
        // re-enable after 10s just in case
        setTimeout(()=>{ btn.disabled=false; btn.innerHTML = btn.dataset.orig; }, 10000);
      }
    });
  });
});

