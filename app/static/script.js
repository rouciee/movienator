// ===== Dropdown Logic
var selectedGenres = [];
var selectedGenresOnLastOpen = [];

var arraysHaveSameElements = function(a, b) {
  return a.length == b.length
         && a.every((element, index)=> element === b[index] );
};

var openDropdown = function() {
  selectedGenresOnLastOpen = selectedGenres.slice(); // create copy of it
  $(".dropdown-content").addClass("show");
  $(".panel").addClass("blur");
  $('.fa-caret-down').toggleClass('rotate');
};

var closeDropdown = function() {
  $(".dropdown-content").removeClass("show");
  $(".panel").removeClass("blur");
  if (!arraysHaveSameElements(selectedGenres.sort(), selectedGenresOnLastOpen.sort())) {
    $(".panel.queue").remove(); // throw out queue.
    fetchNextMovie();
    roll();
  }
  $('.fa-caret-down').toggleClass('rotate');
};

var isRolling = false;
var roll = function() {
  if (isRolling) {
    return;
  }

  isRolling = true;
  maybeFetchAnother();
  $(".current").fadeOut(function() {
    $(this).remove();

    var interval = setInterval(function() {
      if (showAnotherIfPossible()) {
        isRolling = false;
        clearInterval(interval);
      } else {
        $(".spinner").show(); // We might be here a while...
      }
    }, 10);
  });
};

var showAnotherIfPossible = function() {
  var next = $(".panel.queue.img-loaded.vid-loaded");
  if (next.length > 0) {
    next = $(next[0]);

    window.history.pushState({}, '', '/' + next.data('id') + '/');
    $(".spinner").hide();
    next.removeClass("queue");
    next.addClass("current");
    next.fadeIn();
    return true;
  }
  return false;
};

$(document).ready(function() {
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
    roll();
  });
});

var MOVIES_IN_QUEUE = 3;
var maybeFetchAnother = function() {
  var moviesInQueue = $(".panel.queue").length;
  var moviesInQueueFullyLoaded = $(".panel.queue.img-loaded.vid-loaded").length;
  if (moviesInQueue === moviesInQueueFullyLoaded &&
      moviesInQueue < MOVIES_IN_QUEUE) {
    fetchNextMovie();
  }
};

var panelTemplate;
var fetchNextMovie = function() {
  $.get('/random.json?' + $.param({'g': selectedGenres}), function(data) {
    var clone = panelTemplate.clone();
    clone.removeClass("current");
    clone.addClass("queue");
    $("body").append(clone);
    clone.data('id', data.id);
    clone.find("h2 span.title").text(data.title);
    clone.find("h2 span.year").text(data.year);
    clone.find("h4").text(data.genres);
    clone.find("img").attr("src", data.poster_path);
    clone.find("iframe").attr("src", data.youtube_url);
    clone.find('img').on('load', function(e) {
      $(e.target).closest('.panel').addClass('img-loaded');
      maybeFetchAnother();
    });
    clone.find('iframe').on('load', function(e) {
      $(e.target).closest('.panel').addClass('vid-loaded');
      maybeFetchAnother();
    });
  });
};

$(window).on('load', function() {
  panelTemplate = $(".current").clone();
  panelTemplate.removeClass("current");

  $(".spinner").hide();
  $(".current").fadeIn();

  fetchNextMovie();
  initialized = true;
});
