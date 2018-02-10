var ANIMATION_DURATION = 250;
var refreshWithAnimation = function() {
  // Refresh data without full-page reload.  AJAX.
  $.get('/random.json', function(data) {
    // Do this first so that we start fetching poster and video.
    $("h2").text(data.title);
    $("img").attr("src", data.poster_path);
    $("iframe").attr("src", data.youtube_url);

    window.history.pushState({}, '', '/' + data.id + '/');
  });
};

$(document).ready(function() {

  // ===== Attach handlers for dropdown
  $(".dropdown-button").click(function() {
    if ($(".dropdown-content").hasClass("show")) {
      $(".dropdown-content").removeClass("show");
      $(".results-container").removeClass("blur");
      refreshWithAnimation();
    } else {
      $(".dropdown-content").addClass("show");
      $(".results-container").addClass("blur");
    }
  });

  // Close dropdown if user clicks anywhere in the page outside of dropdown.
  $(window).click(function(event) {
    if (!event.target.matches('.dropdown-button') && !event.target.matches('.dropdown-content li') && $('.dropdown-content').hasClass('show')) {
      $(".dropdown-content").removeClass("show");
      $(".results-container").removeClass("blur");
      refreshWithAnimation();
    }
  });

  $(".dropdown-content li").click(function() {
    $(this).toggleClass("active");
  });

  // ===== Attach handler for roll button
  $(".roll").click(function() {
    refreshWithAnimation();
  });
});
