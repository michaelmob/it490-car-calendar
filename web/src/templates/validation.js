// Disable HTML5 validation - using Javascript instead

document.forms.register.noValidation = true;
//-------------------------------------------------------
//Anonymous Function Triggerd by th SUbmit event
//-------------------------------------------------------

$('form').on('submit', function (e) {     
    var elements = this.elements;           
    var valid = {};                          
    var isValid;                             
    var isFormValid;                       

// PERFORM GENERIC CHECKS (calls functions outside the event handler)
    var i;
    for (i = 0, l = elements.length; i < l; i++) {
      // Next line calls validateRequired() validateTypes()
      isValid = validateRequired(elements[i]) && validateTypes(elements[i]); 
      if (!isValid) {                    
        showErrorMessage(elements[i]);   
      } else {                           
        removeErrorMessage(elements[i]); 
      }                                  
      valid[elements[i].id] = isValid;   
    }           
 // PERFORM CUSTOM VALIDATION
    // password (you could cache password input in variable here)
    if (!validatePassword()) {          // Call validatePassword(), and if not valid
      showErrorMessage(document.getElementById('password'));
      valid.password = false;           
    } else {                           
      removeErrorMessage(document.getElementById('password'));
    }

  
    // Loop through valid object, if there are errors set isFormValid to false
    for (var field in valid) {          
      if (!valid[field]) {              
        isFormValid = false;            
        break;                          
      }                                 
      isFormValid = true;               
    }


    // If the form did not validate, prevent it being submitted
    if (!isFormValid) {           
      e.preventDefault();               
    }

  });                                  

// -------------------------------------------------------------------------
  // B) FUNCTIONS FOR GENERIC CHECKS
  // -------------------------------------------------------------------------

  // CHECK IF THE FIELD IS REQUIRED AND IF SO DOES IT HAVE A VALUE
  // Relies on isRequired() and isEmpty() both shown below, and setErrorMessage - shown later.
  function validateRequired(el) {
    if (isRequired(el)) {                          
      var valid = !isEmpty(el);                    
      if (!valid) {                                 
        setErrorMessage(el,  'Field is required');  
      }
      return valid;                                 
    }
    return true;                                    
  }

  // CHECK IF THE ELEMENT IS REQUIRED
  // It is called by validateRequired()
  function isRequired(el) {
   return ((typeof el.required === 'boolean') && el.required) ||
     (typeof el.required === 'string');
  }

  // CHECK IF THE ELEMENT IS EMPTY (or its value is the same as the placeholder text)
  // It is called by validateRequired()
  function isEmpty(el) {
    return !el.value || el.value === el.placeholder;
  }

  // CHECK IF THE VALUE FITS WITH THE TYPE ATTRIBUTE
  // Relies on the validateType object (shown at end of IIFE)
  function validateTypes(el) {
    if (!el.value) return true;                     
                                                    
    var type = $(el).data('type') || el.getAttribute('type'); 
    if (typeof validateType[type] === 'function') { 
      return validateType[type](el);                
    } else {                                        
      return true;                                 
    }
  }

 // Check that the passwords both match and are 8 characters or more
  function validatePassword() {
    var password = document.getElementById('password');
    var valid = password.value.length >= 8;
    if (!valid) {
      setErrorMessage(password, 'Please make sure your password has at least 8 characters');
    }
    return valid;
  }

   // -------------------------------------------------------------------------
  // D) FUNCTIONS TO SET / GET / SHOW / REMOVE ERROR MESSAGES
  // -------------------------------------------------------------------------

  function setErrorMessage(el, message) {
    $(el).data('errorMessage', message);                 // Store error message with element
  }

  function getErrorMessage(el) {
    return $(el).data('errorMessage') || el.title;       // Get error message or title of element
  }

  function showErrorMessage(el) {
    var $el = $(el);                                     // The element with the error
    var errorContainer = $el.siblings('.error.message'); // Any siblings holding an error message

    if (!errorContainer.length) {                         // If no errors exist with the element
       // Create a <span> element to hold the error and add it after the element with the error
       errorContainer = $('<span class="error message"></span>').insertAfter($el);
    }
    errorContainer.text(getErrorMessage(el));             // Add error message
  }

  function removeErrorMessage(el) {
    var errorContainer = $(el).siblings('.error.message'); // Get the sibling of this form control used to hold the error message
    errorContainer.remove();                               // Remove the element that contains the error message
  }

// -------------------------------------------------------------------------
  // E) OBJECT FOR CHECKING TYPES
  // -------------------------------------------------------------------------

  // Checks whether data is valid, if not set error message
  // Returns true if valid, false if invalid
  var validateType = {
    email: function (el) {                                 // Create email() method
      // Rudimentary regular expression that checks for a single @ in the email
      var valid = /[^@]+@[^@]+/.test(el.value);            // Store result of test in valid
      if (!valid) {                                        // If the value of valid is not true
        setErrorMessage(el, 'Please enter a valid email'); // Set error message
      }
      return valid;                                        // Return the valid variable
    },

     number: function (el) {                                // Create number() method
      var valid = /^\d+$/.test(el.value);                  // Store result of test in valid
      if (!valid) {
        setErrorMessage(el, 'Please enter a valid number');
      }
      return valid;
    },
    date: function (el) {                                  // Create date() method
                                                           // Store result of test in valid
      var valid = /^(\d{2}\/\d{2}\/\d{4})|(\d{4}-\d{2}-\d{2})$/.test(el.value);
      if (!valid) {                                        // If the value of valid is not true
        setErrorMessage(el, 'Please enter a valid date');  // Set error message
      }
      return valid;                                        // Return the valid variable
    }
  };
();  // End of IIFE





