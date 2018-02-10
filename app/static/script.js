var imgLoaded = false;
var videoLoaded = false;

var ANIMATION_DURATION = 250;
var refreshWithAnimation = function() {
  // Refresh data without full-page reload.  AJAX.
  $.get('/random.json', function(data) {
    // Do this first so that we start fetching poster and video.
    $("#two img").attr("src", data.poster_path);
    $("#two iframe").attr("src", data.youtube_url);
    $("#two h2 span.title").text(data.title);
    $("#two h2 span.year").text(data.year);
    $("#two h4").text(data.genres);

    $("#one").fadeOut();
    window.history.pushState({}, '', '/' + data.id + '/');
  });
};

var maybeDoSwitch = function() {
  if (imgLoaded && videoLoaded) {
    $("#two").fadeIn(400, function() {
      // Reset variables.
      $("#one").prop("id", "tmp");
      $("#two").prop("id", "one");
      $("#tmp").prop("id", "two");
      imgLoaded = false;
      videoLoaded = false;
    });
  }
};

$(window).on('load', function() {
  $('img').on('load', function() {
    imgLoaded = true;
    maybeDoSwitch()
  });
  $('iframe').on('load', function() {
    videoLoaded = true;
    maybeDoSwitch()
  });

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
