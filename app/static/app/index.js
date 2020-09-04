setTimeout(function(){
    $('#news-letter-container').css({'visibility':'visible','opacity':'1'});
    $('body').css('overflow','hidden');
    console.log("alright");
},2000);

// A function that will close the news letter container when clicked on
let closeNewsLetter = (url) => {
    let emailRegExp = /^[a-z][a-z\d]+@[a-z]+\.[a-z]{2,}(\.[a-z]{2,})?$/
    // When the close button is clicked
    $('#news-letter div').first().click(function(){
        $('#news-letter-container').css({'visibility':'hidden','opacity':'0'});
        $('body').css('overflow','auto');
    });
    // When the subscribe button is clicked
    $('#subscribe').click(function(){
        let email = $('#email'); // Get the email
        console.log(email)
        // Check if it is a valid email
        if(emailRegExp.test(email.val())){
            // Make an ajax request
            $.ajax({
                url: url,
                data: {
                    "email": email.val()
                },
                dataType: 'json'
            });
        }
        // Reset the input fields value
        email.val('');
        // Remove the news letters
//        $('#news-letter-container').css({'visibility':'hidden','opacity':'0'});
//        $('body').css('overflow','auto');
        
    });
}


// A function that adds a good to the users cart
let addToCart = (url) => {
    // Add to cart functionality for homa page goods and other goods page
    $('.good > p').click(function(){
        let ele = $(this)
        if(ele.text() === "ADD TO CART" && !ele.attr('class')){
            let productId = $(this).attr('id')
            $.ajax({
                url: url,
                data: {
                    "quantity": 1,
                    productId
                },
                dataType: 'json',
                crossOrigin: true,
                success: function(data){
                    console.log(data)
                    console.log("hmmm")
                    // Modify the number of items in the cart on the frontend
                    $('#cart a span').text(`${data['cart_items']}`);
                    ele.text("ADDED");

                }
            });   
        }
    });
    // Add to cart functionality for main item page
    $('#qty-container').parent().find('p').last().click(function(){
        let ele = $(this)
        let quantity = $(this).parent().find('#qty').text();
        if(ele.text() === "ADD TO CART"){
            let productId = $(this).attr('id')
            $.ajax({
                url: url,
                data: {
                    quantity,
                    productId
                },
                dataType: 'json',
                crossOrigin: true,
                success: function(data){
                    // Modify the number of items in the cart on the frontend
                    $('#cart a span').text(`${data['cart_items']}`);
                    ele.text("ADDED");
                }
            });   
        }
    });
}
