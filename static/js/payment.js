//'use strict';

var stripe = Stripe('sk_test_51Kv2hzLv560bXuLqqPRoiDxhSgMLaoUc9FvavcbuoCNd5IXRfD5yqZ7U1EI8ApyiWd7yvpmdbbjYtWW7OoAs3F6F00LyB4rDmb');

var elem = document.getElementById('submit');
clientSecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
  base: {
    color: "#000",
    lineHeight: '2.4',
    fontSize: '16px'
  }
};


var card = elements.create("card", {
  style: style
});
card.mount("#card-element");

card.on('change', function (event) {
  var displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
  ev.preventDefault();

  var customerName = document.getElementById("customerName").value;
  var customerAddress = document.getElementById("customerAddress").value;
  var customerAddress2 = document.getElementById("customerAddress2").value;
  var postCode = document.getElementById("postCode").value;


  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
      order_key: clientSecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
    },
    success: function (json) {
      console.log(json.success)

      stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
            address: {
              line1: customerAddress,
              line2: customerAddress2
            },
            name: customerName
          },
        }
      }).then(function (result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')

            window.location.replace("http://127.0.0.1:8000/payment/order-placed/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) {},
  });



});