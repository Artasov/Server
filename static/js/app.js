const { log } = console;



var form_inputs = document.getElementsByClassName('form-input');


function changed_input(index) {
   var field_names= document.getElementsByClassName('reg-form__field-name');
   for (let i = 0; i < field_names.length; i++) {
      field_names[i].classList.remove('_active_field');
   }
   for (let i = 0; i < form_inputs.length; i++) {
      form_inputs[i].classList.remove('_active_input');
   }
   form_inputs[index].parentNode.getElementsByClassName('reg-form__field-name')[0].classList.add('_active_field');
   form_inputs[index].classList.add('_active_input');

   for (let i = 0; i < form_inputs.length; i++){
      if (form_inputs[i].value != "") {
         form_inputs[i].parentNode.classList.add('_done_field');
      }
      else {
         form_inputs[i].parentNode.classList.remove('_done_field');
      }
   }
}


function click_on_radio(index) {
   for (let i = 0; i < form_inputs.length; i++){
      if (form_inputs[i].value != "") {
         form_inputs[i].parentNode.classList.add('_done_field');
      }
      else {
         form_inputs[i].parentNode.classList.remove('_done_field');
      }
   }
   var field_names = document.getElementsByClassName('reg-form__field-name');
   for (let i = 0; i < field_names.length; i++) {
      field_names[i].classList.remove('_active_field');
   }
   for (let i = 0; i < form_inputs.length; i++) {
      form_inputs[i].classList.remove('_active_input');
   }

   
   radios = document.getElementsByClassName('radio');
   gender_title = document.getElementsByClassName('gender-title');
   for (let i = 0; i < radios.length; i++) {
      radios[i].checked = false
      gender_title[i].style.color = 'rgba(255, 255, 255, 0.3)';
   }
   radios[index].checked = true
   gender_title[index].style.color = '#ff4d5c';
   document.getElementsByClassName('reg-form__field-name-gender')[0].style.color = '#ff4d5c';
   document.getElementsByClassName('reg-form__gender-field')[0].style.border = '2px solid #ff4d5c';
   document.getElementsByClassName('reg-form__gender-field')[0].classList.add('_done_gender_field');
}


function close_warning() {
   document.getElementsByClassName('warning')[0].style.bottom = '-100%';
}