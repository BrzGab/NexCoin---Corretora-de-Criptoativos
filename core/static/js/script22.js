document.getElementById('amount-brl').addEventListener('input', calculateExchange);
document.getElementById('crypto-select').addEventListener('change', calculateExchange);

function calculateExchange() {
    const brlAmount = parseFloat(document.getElementById('amount-brl').value);
    const selectedCrypto = document.getElementById('crypto-select');
    const cryptoRate = parseFloat(selectedCrypto.options[selectedCrypto.selectedIndex].dataset.rate);
    
    if (!isNaN(brlAmount) && !isNaN(cryptoRate)) {
        const cryptoAmount = brlAmount * cryptoRate;
        document.getElementById('crypto-output').value = cryptoAmount.toFixed(8);
    } else {
        document.getElementById('crypto-output').value = '';
    }
}

document.getElementById('exchange-btn').addEventListener('click', function() {
    alert('Compra realizada com sucesso, visite sua carteira!');
});

document.addEventListener('DOMContentLoaded', function() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    const quotesSection = document.getElementById('quotes-section');
  
    scrollIndicator.addEventListener('click', function() {
      quotesSection.scrollIntoView({ behavior: 'smooth' });
    });

    document.addEventListener("DOMContentLoaded", function() {
      const navToggleBtn = document.querySelector(".nav-toggle-btn");
      const navbar = document.querySelector(".navbar");
    
      navToggleBtn.addEventListener("click", function() {
          navbar.classList.toggle("active");
      });
    });
    
  
    // Ocultar o indicador de rolagem quando a seção de cotações estiver visível
    window.addEventListener('scroll', function() {
      const rect = quotesSection.getBoundingClientRect();
      if (rect.top <= window.innerHeight / 2) {
        scrollIndicator.style.opacity = '0';
        scrollIndicator.style.pointerEvents = 'none';
      } else {
        scrollIndicator.style.opacity = '0.7';
        scrollIndicator.style.pointerEvents = 'auto';
      }
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
  const canvas = document.getElementById('animatedBackground');
  const ctx = canvas.getContext('2d');
  
  // Configuração do canvas
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  // Criação das partículas
  const particles = [];
  const particleCount = 100;

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 2 + 1,
      dx: (Math.random() - 0.5) * 0.5,
      dy: (Math.random() - 0.5) * 0.5,
    });
  }

  // Animação das partículas
  function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';

    particles.forEach(particle => {
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fill();

      particle.x += particle.dx;
      particle.y += particle.dy;

      if (particle.x < 0 || particle.x > canvas.width) particle.dx *= -1;
      if (particle.y < 0 || particle.y > canvas.height) particle.dy *= -1;
    });

    requestAnimationFrame(animateParticles);
  }

  animateParticles();

  // Lógica de compra
  const form = document.getElementById('purchase-form');
  const amountBRL = document.getElementById('amount-brl');
  const cryptoSelect = document.getElementById('crypto-select');
  const cryptoOutput = document.getElementById('crypto-output');

  function updateCryptoOutput() {
    // Simulação de taxa de câmbio (substitua por uma API real em produção)
    const exchangeRates = {
      bitcoin: 0.0000056,  // 1 BRL = 0.0000056 BTC
      ethereum: 0.000089,  // 1 BRL = 0.000089 ETH
      litecoin: 0.0021     // 1 BRL = 0.0021 LTC
    };

    const brlValue = parseFloat(amountBRL.value);
    const selectedCrypto = cryptoSelect.value;

    if (!isNaN(brlValue) && selectedCrypto in exchangeRates) {
      const cryptoAmount = brlValue * exchangeRates[selectedCrypto];
      cryptoOutput.value = cryptoAmount.toFixed(8);
    } else {
      cryptoOutput.value = '';
    }
  }

  amountBRL.addEventListener('input', updateCryptoOutput);
  cryptoSelect.addEventListener('change', updateCryptoOutput);

  form.addEventListener('submit', function(event) {
    event.preventDefault();
    // Aqui você pode adicionar a lógica para processar a compra
    // Por exemplo, enviar os dados para o backend Django
    console.log('Compra processada:', {
      valorBRL: amountBRL.value,
      criptomoeda: cryptoSelect.value,
      quantidadeCripto: cryptoOutput.value
    });
  });
});

'use strict';



/**
 * add event on element
 */

const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
}



/**
 * navbar toggle
 */

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");

const toggleNavbar = function () {
  navbar.classList.toggle("active");
  navToggler.classList.toggle("active");
  document.body.classList.toggle("active");
}

addEventOnElem(navToggler, "click", toggleNavbar);

const closeNavbar = function () {
  navbar.classList.remove("active");
  navToggler.classList.remove("active");
  document.body.classList.remove("active");
}

addEventOnElem(navbarLinks, "click", closeNavbar);



/**
 * header active
 */

const header = document.querySelector("[data-header]");

const activeHeader = function () {
  if (window.scrollY > 300) {
    header.classList.add("active");
  } else {
    header.classList.remove("active");
  }
}

addEventOnElem(window, "scroll", activeHeader);



/**
 * toggle active on add to fav
 */

const addToFavBtns = document.querySelectorAll("[data-add-to-fav]");

const toggleActive = function () {
  this.classList.toggle("active");
}

addEventOnElem(addToFavBtns, "click", toggleActive);



/**
 * scroll revreal effect
 */

const sections = document.querySelectorAll("[data-section]");

const scrollReveal = function () {
  for (let i = 0; i < sections.length; i++) {
    if (sections[i].getBoundingClientRect().top < window.innerHeight / 1.5) {
      sections[i].classList.add("active");
    } else {
      sections[i].classList.remove("active");
    }
  }
}

scrollReveal();

addEventOnElem(window, "scroll", scrollReveal);


