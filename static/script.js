console.log('loaded');
(function (){
    console.log("beginning")
    var user_id = window.imagefave_uid
    var image_filename_regex = /png|jpe?g|gif/
    var url_prefix = "http://localhost:5000/fave/"

    function big_enough(image){
        return image.width() > 250 && image.height() > 250
    }

    var tracking_pixel = new Image()
    function send_rating(source){
        url = url_prefix + user_id + '/' + source
        tracking_pixel.src = url
    }
    
    var images = $('img')
    console.log("images", images)
    _.each(images.toArray(),function(image){
        var image = $(image)
        console.log("Image", image)
        // Is it a link to another (hopefully larger) image?
        var parent = image.parents('a:first')
        if(parent.length && parent.attr('href').match(image_filename_regex)){
            console.log("A parent was found")
            var source = parent.attr('href')

        // Is it big enough?
        } else if (big_enough(image)) {
            console.log("It was big enough")
            var source = image.attr('src')
        }

        else {
            console.log("UH OH!")
            return;
        }

        // Make the UI
        var ui = $('<p><a>Fave</a></p>')
        ui.click(function(event){
            event.preventDefault()
            send_rating(source)
            ui.html("<p>Faved</p>")
            ui.unbind('click')
        })
        image.before(ui)
        console.log(ui)
    })
})()
