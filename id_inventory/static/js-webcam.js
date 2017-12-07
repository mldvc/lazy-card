$("document").ready ( function () {

	// Webcam.set({
	// 	// live preview size
	// 	width: 320,
	// 	height: 240,
		
	// 	// device capture size
	// 	dest_width: 320,
	// 	dest_height: 240,
		
	// 	// final cropped size
	// 	crop_width: 163,
	// 	crop_height: 223,
		
	// 	// format and quality
	// 	image_format: 'jpeg',
	// 	jpeg_quality: 100
	// });

	// Webcam.attach( '#idpicture' );

 //    $('#take-pic').click( function() {
 //        // take snapshot and get image data
 //        Webcam.snap( function(data_uri) {
 //            // display results in page
 //            $('#btnSavePicToPC').attr('href', data_uri);
 //            $('#result-picture').attr('src', data_uri);
 //        } );
 //    });

    // var readUrl = function(input) {
    //     if (input.files && input.files[0]) {
    //         var reader = new FileReader();
    //         reader.onload = function (e) {
    //             $('#sig-preview').attr('src', e.target.result);
    //         };
    //         reader.readAsDataURL(input.files[0]);
    //     }
    // }

    // $("#sig-upload").change( function() {
    // 	readUrl($(this));
    // });

    $('#btnSigPreview').click( function() {
        var canvas = document.getElementById("result-sig"),
            x = parseInt($('#result-sig').attr('x')),
            y = parseInt($('#result-sig').attr('y')),
            ctx = canvas.getContext("2d"),
            image = document.getElementById("sig-preview");

        canvas.width = x;
        canvas.height = y;
        ctx.drawImage(image,0,0);
            
        var imgd = ctx.getImageData(0, 0, x, y),
            pix = imgd.data,
            newColor = {r:0,g:0,b:0, a:0};
            newColorBlack = {r:255,g:255,b:255, a:255};

        for (var i = 0, n = pix.length; i <n; i += 4) {
            var r = pix[i],
                g = pix[i+1],
                b = pix[i+2];

            if(r == 255&& g == 255 && b == 255){ 
                // Change the white to the new color.
                pix[i] = newColor.r;
                pix[i+1] = newColor.g;
                pix[i+2] = newColor.b;
                pix[i+3] = newColor.a;
            }

            if ($("#sig-preview").attr("type").toLowerCase().indexOf("alumni") < 0 && 
                $("#sig-preview").attr("type").toLowerCase().indexOf("hospital") < 0) {
                if (r == 0 && g == 0 && b == 0) { 
                    // Change the black to the new color.
                    pix[i] = newColorBlack.r;
                    pix[i+1] = newColorBlack.g;
                    pix[i+2] = newColorBlack.b;
                    pix[i+3] = newColorBlack.a;
                }
            }
        }

        ctx.putImageData(imgd, 0, 0);
    });

    if ( $('.name-wrapper').length ) {
    	while ($('.name-wrapper').height() != 42) {
    		var currentSize = parseInt($('#name').css('font-size'))
    		currentSize -= 1;
    		$('#name').css("font-size", currentSize + "px")
    	}
    }

    if ( $('.under-name-wrapper').length ) {
    	while ($('.under-name-wrapper').height() != 24) {
    		var currentSize = parseInt($('#under-name').css('font-size'))
    		currentSize -= 1;
    		$('#under-name').css("font-size", currentSize + "px")
    	}
    }

    if ( $('.address-wrapper').length ) {
    	while ($('.address-wrapper').height() != 21) {
    		var currentSize = parseInt($('#address').css('font-size'))
    		currentSize -= 1;
    		$('#address').css("font-size", currentSize + "px")
    	}
    }

    if ( $('.cnum-wrapper.alumni').length ) {
		while ($('.cnum-wrapper.alumni').width() != 140) {
			var currentSize = parseInt($('#cnum').css('font-size'))
			currentSize -= 1;
			$('#cnum').css("font-size", currentSize + "px")
		}
	}

    if ( $('.unit-wrapper.employee').length ) {
        while ($('.unit-wrapper.employee').height() != 21) {
            var currentSize = parseInt($('#unit').css('font-size'))
            currentSize -= 1;
            $('#unit').css("font-size", currentSize + "px")
        }
    }

	$('#box1-up').click( function() {
		var currTop = parseInt($('#result-sig').css('top'))
		currTop -= 2;
		$('#result-sig').css("top", currTop + "px")
	});

	$('#box1-left').click( function() {
		var currLeft = parseInt($('#result-sig').css('left'))
		currLeft -= 2;
		$('#result-sig').css("left", currLeft + "px")
	});

	$('#box1-right').click( function() {
		var currRight = parseInt($('#result-sig').css('left'))
		currRight += 2;
		$('#result-sig').css("left", currRight + "px")
	});

	$('#box1-down').click( function() {
		var currDown = parseInt($('#result-sig').css('top'))
		currDown += 2;
		$('#result-sig').css("top", currDown + "px")
	});

	$("#id_id_type, label[for='id_id_type']").css("display", "none")



	// FOR SELECTING ID LAYOUT
    // var funcGetLayout = function() {
    //     var form = $("#id-layout").closest("form");
    //     $.ajax({
    //         url: form.attr("url"),
    //         data: form.serialize(),
    //         dataType: 'json',
    //         success: function (data) {
				// $.each( data, function( k, v ) {
				// 	if (k == 'layout-front') {
    //                     if ( $('#portrait-front').length ) {
    //                         $('#portrait-front').attr('src', v)
    //                     } else {
    //                         $('#student-front').attr('src', v)
    //                     }
				// 	} else {
    //                     if ( $('#portrait-back').length ) {
    //                         $('#portrait-back').attr('src', v)
    //                     } else {
    //                         $('#student-back').attr('src', v)
    //                     }
				// 	};
				// });
    //         }
    //     });
    // }
    // $("#id-layout").change(funcGetLayout)
    // $("document").ready(funcGetLayout)
	// #FOR SELECTING ID LAYOUT

    $( function() {
        $( ".pic-control-wrapper" ).draggable();
        $( ".sig-controls" ).draggable();
        $( ".layout-selector-wrapper" ).draggable();
        $( ".form-fields" ).draggable();
        $( "#result-picture" ).draggable();
    });


    (function() {
        var beforePrint = function() {
            console.log('Functionality to run before printing.');
        };
        var afterPrint = function() {
            $( function() {
                $( "#dialog-confirm" ).dialog({
                    resizable: false,
                    height: "auto",
                    width: 400,
                    modal: true,
                    buttons: {
                        "Add to print history": function() {
                            $("#add-history")[0].click();
                        },
                        Cancel: function() {
                            $( this ).dialog( "close" );
                        }
                    }
                });
            });
        };

        if (window.matchMedia) {
            var mediaQueryList = window.matchMedia('print');
            mediaQueryList.addListener(function(mql) {
                if (mql.matches) {
                    beforePrint();
                } else {
                    afterPrint();
                }
            });
        }

        window.onbeforeprint = beforePrint;
        window.onafterprint = afterPrint;
    }());

    // picture zoom slider
    $( function() {
        $( "#zoom-slider" ).slider({
            range: "max",
            min: 1,
            max: 200,
            value: 150,
            slide: function( event, ui ) {
                $( "#result-picture" ).css( "height", ui.value + "%");
            }
        });
      } );


});