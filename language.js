"use strict";
(() => {
const bar=document.querySelector('.language-switch');if(!bar)return;
bar.querySelectorAll('[data-language]').forEach(link=>link.addEventListener('click',()=>{try{localStorage.setItem('tarek-portfolio-language',link.dataset.language)}catch{}}));
document.querySelectorAll('[data-language]').forEach(link=>link.addEventListener('click',()=>{try{localStorage.setItem('tarek-portfolio-language',link.dataset.language)}catch{}}));
try { const saved=localStorage.getItem('tarek-portfolio-language');const current=document.documentElement.lang;if((saved==='en'||saved==='fr')&&saved!==current){const target=bar.querySelector('[data-language="'+saved+'"]');if(target){const url=new URL(target.href);url.hash=location.hash;location.replace(url.href);}} } catch {}
})();
