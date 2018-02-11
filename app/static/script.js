var imgLoaded = false;
var videoLoaded = false;
var selectedGenres = [];
var selectedGenresOnLastOpen = [];

var ANIMATION_DURATION = 250;

var arraysHaveSameElements = function(a, b) {
  return a.length == b.length
         && a.every((element, index)=> element === b[index] );
};

var refreshWithAnimation = function() {
  // Refresh data without full-page reload.  AJAX.
  $.get('/random.json?' + $.param({'g': selectedGenres}), function(data) {
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
    $("#two").fadeIn(function() {
      // Reset variables.
      $("#one").prop("id", "tmp");
      $("#two").prop("id", "one");
      $("#tmp").prop("id", "two");
      imgLoaded = false;
      videoLoaded = false;
    });
  }
};

var openDropdown = function() {
  selectedGenresOnLastOpen = selectedGenres.slice(); // create copy of it
  $(".dropdown-content").addClass("show");
  $(".panel").addClass("blur");
};

var closeDropdown = function() {
  $(".dropdown-content").removeClass("show");
  $(".panel").removeClass("blur");
  if (!arraysHaveSameElements(selectedGenres.sort(), selectedGenresOnLastOpen.sort())) {
    refreshWithAnimation();
  }
};

$(window).on('load', function() {
  $("#one").fadeIn();
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
      closeDropdown();
    } else {
      openDropdown();
    }
  });

  // Close dropdown if user clicks anywhere in the page outside of dropdown.
  $(window).click(function(event) {
    if (!event.target.matches('.dropdown-button') &&
        !event.target.matches('.dropdown-content li') &&
        $('.dropdown-content').hasClass('show')) {
      closeDropdown();
    }
  });

  $(".dropdown-content li").click(function() {
    var key = $(this).text();
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      // Remove from array.
      var index = selectedGenres.indexOf(key);
      if (index > -1) {
        selectedGenres.splice(index, 1);
      }
    } else {
      $(this).addClass("active");
      selectedGenres.push(key);
    }
  });

  // ===== Attach handler for roll button
  $(".roll").click(function() {
    refreshWithAnimation();
  });
});
