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
    fetchNextMovie(); // B.C. when no movies in queue, can wait forever.
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
  // TODO: Check if this should be checked/done after roll is shown.
  if ($(".panel.queue.img-loaded.vid-loaded").length === MOVIES_IN_QUEUE) {
    fetchNextMovie();
  } // else should be chain-fetching.
  $(".current").fadeOut(function() {
    $(this).remove(); // TODO: Hide and stop playing video.  "Cache" back button.

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
      moviesInQueue < MOVIES_IN_QUEUE &&
      moviesInQueue > 0) {
    fetchNextMovie();
  }
};

var movieIdFromPath = function() {
  var path = window.location.pathname;
  return path.substring(1, path.length - 1);
};

var panelTemplate;
var fetchNextMovie = function(pk) {
  var url = pk === undefined ? '/random.json?' + $.param({'g': selectedGenres}) : '/'+pk+'.json';
  $.get(url, function(data) {
    var clone = panelTemplate.clone();
    if (pk === undefined) {
      clone.addClass("queue");
    } else {
      clone.addClass("current");
    }

    clone.data('id', data.id);
    clone.addClass("movie-"+data.id);
    clone.find(".genres-text").text(data.genres);
    clone.find("img").attr("src", data.poster_path);
    clone.find("iframe").attr("src", data.youtube_url + "?showinfo=0");
    clone.find('img').on('load', function(e) {
      $(e.target).closest('.panel').addClass('img-loaded');  // NOTE: This can be done in closure here?
      if (pk === undefined) {
        maybeFetchAnother();
      } else if (
        $(e.target).closest('.panel').hasClass("vid-loaded") &&
        parseInt(movieIdFromPath()) === data.id
      ) {
        $(".spinner").hide();
        clone.fadeIn(); // Show IFF still at same location.
      }
    });
    clone.find('iframe').on('load', function(e) {
      $(e.target).closest('.panel').addClass('vid-loaded');
      if (pk === undefined) {
        maybeFetchAnother();
      } else if (
        $(e.target).closest('.panel').hasClass("img-loaded") &&
        parseInt(movieIdFromPath()) === data.id
      ) {
        $(".spinner").hide();
        clone.fadeIn(); // Show IFF still at same location.
      }
    });
    $("body").append(clone);
  });
};

$(window).on('load', function() {
  panelTemplate = $(".current").clone();
  panelTemplate.removeClass("current");
  panelTemplate.removeClass("movie-"+movieIdFromPath());

  $(".spinner").hide();
  $(".current").fadeIn();

  fetchNextMovie();
  initialized = true;
});

window.onpopstate = function(event) {
  // Back or Forward button was pressed.
  var movieId = movieIdFromPath();

  // Hide everything. (Show spinner)
  $(".panel").fadeOut();
  $(".spinner").show();
  $(".current").removeClass("current");

  // If exists; show.  TODO: Set current.
  if ($(".movie-"+movieId).length > 0) {
    $(".spinner").hide();
    $(".movie-"+movieId).addClass("current").fadeIn();
  } else {
    // Else fetch, and eventually show (if nothing else happened).
    fetchNextMovie(movieId);
  }
};
