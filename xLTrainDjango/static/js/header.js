let reg_active = false;

function sleep(ms) {
   return new Promise(resolve => setTimeout(resolve, ms));
}

function check_mobile() {
   const isMobile = {
      Android: function () {
         return navigator.userAgent.match(/Android/i);
      },
      BlackBerry: function () {
         return navigator.userAgent.match(/BlackBerry/i);
      },
      IOS: function () {
         return navigator.userAgent.match(/iPhone|iPad|iPod/i);
      },
      Opera: function () {
         return navigator.userAgent.match(/Opera Mini/i);
      },
      Windows: function () {
         return navigator.userAgent.match(/IEMobile/i);
      },
      any: function () {
         return (
            isMobile.Android() ||
            isMobile.BlackBerry() ||
            isMobile.IOS() ||
            isMobile.Opera() ||
            isMobile.Windows()
         );
      }
   };

   if (isMobile.any()) {
      document.body.classList.add('_touch');
      if(document.getElementsByClassName('menu__burger-btn').length!==0){
         document.getElementsByClassName('menu__burger-btn')[0].addEventListener('click', function (e) {
            if (reg_active === true) {
               document.getElementsByClassName('wrapper')[0].classList.remove('_active_reg-form');
               reg_active = false
            }
            else {
               document.getElementsByTagName('header')[0].classList.toggle('_when-menu-on');
               document.getElementsByClassName('header__menu')[0].classList.toggle('_active_menu');
               document.getElementsByClassName('wrapper')[0].classList.remove('_active_reg-form');
            }
            document.getElementsByClassName('body')[0].classList.toggle('_active_menu_OnBody');
         });
      }
   }
   else {
      document.body.classList.add('_pc');
      if(document.getElementsByClassName('menu__burger-btn').length !== 0){
         document.getElementsByClassName('menu__burger-btn')[0].style.display = 'none';
      }
   }
}

try {
   document.getElementsByClassName('close_icon-reg')[0].addEventListener('click', function (e) {
      document.getElementsByClassName('wrapper')[0].classList.remove('_active_reg-form');
      reg_active = false
   })
   document.getElementsByClassName('btn_reg')[0].addEventListener('click', function (e) {
      document.getElementsByClassName('menu__burger-btn')[0].click();
      document.getElementsByClassName('wrapper')[0].classList.add('_active_reg-form');
      document.getElementsByClassName('body')[0].classList.toggle('_active_menu_OnBody');
      reg_active = true
   });
}catch (e) {}

check_mobile();
// document.getElementsByClassName('header__logo')[0].src = 'img/LOGO.png';
// document.getElementsByClassName('close_icon-reg')[0].src = '/img/close.png';
// document.getElementsByClassName('main__content-ava')[0].src = '/img/AVA.jpg';
// document.getElementsByClassName('close-icon-reg-warning')[0].src = '/img/close.png';

var ico_down = document.getElementsByClassName('ico-up-down');
for (let i = 0; i < ico_down.length; i++) {
   ico_down[i].addEventListener('click', async function (e) {
      if (ico_down[i].classList.contains('fa-chevron-down')) {    
         ico_down[i].parentNode.parentNode.getElementsByClassName('info__el-description-text')[0].style.display = 'block';
         await sleep(0);
         ico_down[i].parentNode.parentNode.getElementsByClassName('info__el-description-text')[0].style.height = '100%';
         ico_down[i].classList.remove('fa-chevron-down');
         ico_down[i].classList.add('fa-chevron-up');
      }
      else {
         ico_down[i].parentNode.parentNode.getElementsByClassName('info__el-description-text')[0].style.height = '0%';
         await sleep(400);
         ico_down[i].parentNode.parentNode.getElementsByClassName('info__el-description-text')[0].style.display = 'none';
         ico_down[i].classList.add('fa-chevron-down');
         ico_down[i].classList.remove('fa-chevron-up');
      }
   });
}
