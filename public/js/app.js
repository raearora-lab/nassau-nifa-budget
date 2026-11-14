(function(){
  function group(sel, attr, apply){
    var wrap=document.querySelector(sel); if(!wrap) return;
    wrap.addEventListener('click',function(e){
      var b=e.target.closest('button'); if(!b) return;
      wrap.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b?'true':'false');});
      apply(b.getAttribute(attr));
    });
  }
  group('[data-group="cat"]','data-cat',function(c){
    document.querySelectorAll('#figs tbody tr').forEach(function(r){r.hidden=r.getAttribute('data-cat')!==c;});
  });
  group('[data-group="view"]','data-view',function(v){
    document.querySelectorAll('[data-viewtable]').forEach(function(t){t.hidden=t.getAttribute('data-viewtable')!==v;});
  });
})();
