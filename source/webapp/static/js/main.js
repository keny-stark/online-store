$('.js-button-campaign').click(function() {
	$('.js-overlay-campaign').fadeIn();
	$('.js-overlay-campaign').addClass('disabled');
});
$('.js-close-campaign').click(function() {
	$('.js-overlay-campaign').fadeOut();
});


$(document).mouseup(function (e) {
	var popup = $('.js-popup-campaign');
	if (e.target!=popup[0]&&popup.has(e.target).length === 0){
		$('.js-overlay-campaign').fadeOut();
	}
});

$('.js-button-campaign_2').click(function() {
	$('.js-overlay-campaign_2').fadeIn();
	$('.js-overlay-campaign_2').addClass('disabled');
});
$('.js-close-campaign_2').click(function() {
	$('.js-overlay-campaign_2').fadeOut();
});
