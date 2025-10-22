document.addEventListener('DOMContentLoaded', ()=>{
  const yearEl = document.getElementById('year');
  if(yearEl) yearEl.textContent = new Date().getFullYear();

  const themeToggle = document.getElementById('theme-toggle');
  themeToggle && themeToggle.addEventListener('click', ()=>{
    document.documentElement.classList.toggle('light');
  });
});
