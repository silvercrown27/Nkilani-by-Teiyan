
var paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener('submit', payWithPaystack, false);

function payWithPaystack() {
    var handler = PaystackPop.setup({
        key: 'YOUR_PUBLIC_KEY', // Replace with your public key
        email: document.getElementById('email-address').value,
        amount: document.getElementById('amount').value * 100, // Convert to lowest currency unit
        currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars
        ref: 'YOUR_REFERENCE', // Replace with a reference you generated
        callback: function(response) {
            var reference = response.reference;
            alert('Payment complete! Reference: ' + reference);
            // Make an AJAX call to your server with the reference to verify the transaction
            $.post('/verify-payment', { reference: reference }, function(data) {});
        },
        onClose: function() {
          alert('Transaction was not completed, window closed.');
        },
    });
    handler.openIframe();
}
