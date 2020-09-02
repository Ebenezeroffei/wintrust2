//setTimeout(function(){
//    $('#news-letter-container').css({'visibility':'visible','opacity':'1'});
//    $('body').css('overflow','hidden');
//},2000)

// A function that will close the news letter container when clicked on
let closeNewsLetter = () => {
    $('#news-letter div').first().click(function(){
        $('#news-letter-container').css({'visibility':'hidden','opacity':'0'});
        $('body').css('overflow','auto');
    });
}

closeNewsLetter()


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
