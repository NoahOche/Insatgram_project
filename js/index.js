$(document).ready(() => {

  $('#userMenuButton').click(() => {
    $('#userMenu').toggleClass('hidden')
    $('#uploadForm').addClass('hidden')
  })

  $('#uploadButton').click(() => {
    $('#uploadForm').toggleClass('hidden')
    $('#userMenu').addClass('hidden')
  })
  $('i[id^=post-]').click(function () {
  
    let id = /post-([0-9A-Za-z\-]+)$/.exec($(this).attr('id'))[1]

    fetch(`/like-post/?post_id=${id}`)
      .then(response => response.json())
      .then(data => {
        let images = ''
        let counter = 0
        let likes = data['likes']
        for (let liker in likes) {
          if (data['user_profile'] === likes[liker].id_user) {
            if($(this).hasClass("far fa-heart")) {
              $(this).removeClass("far fa-heart").addClass("fas fa-heart");
            } else {
              $(this).removeClass("fas fa-heart").addClass("far fa-heart");
            }
          }

        }
        if($(this).hasClass("far")) {
          $(this).removeClass("far").addClass("fas");
        } else {
          $(this).removeClass("fas").addClass("far");
        }

        for (let liker in likes) {
          if (counter === 2) {
            break
          }
          let image = likes[liker].profile_img
          
          images += `
          <figure class='avatar avatar-sm '>
          <img src="/media/${image}" /> 
          </figure>`
          counter++

        }
      
        

        $(`#like-images-${data['post_id']}`).html(images)
        $(`#likes-no-${data['post_id']}`).html(`Liked by ${likes.length} people`)
      })
  })

  // setInterval(() => {

  // }, 5000);

  $('#chat').click(function () {
    let user = $('#user').val()
    let profile = $('#my_profile').val()
    fetch(`/Jsonchat/?user_id=${user}`)
      .then(response => response.json())
      .then(data => {
        alert(user)
        // let images = ''
        // let counter = 0
        // let likes = data['likes']
        // for (let liker in likes) {
        //   if (data['user_profile'] === likes[liker].id_user) {
        //     if($(this).hasClass("far fa-heart")) {
        //       $(this).removeClass("far fa-heart").addClass("fas fa-heart");
        //     } else {
        //       $(this).removeClass("fas fa-heart").addClass("far fa-heart");
        //     }
        //   }

        // }
        // if (likes.length === 0 ){
        //   if($(this).hasClass("far fa-heart")) {
        //     $(this).removeClass("far fa-heart").addClass("fas fa-heart");
        //   } else {
        //     $(this).removeClass("fas fa-heart").addClass("far fa-heart");
        //   }

        // }
        // for (let liker in likes) {
        //   if (counter === 2) {
        //     break
        //   }
        //   let image = likes[liker].profile_img
          
        //   images += `
        //   <figure class='avatar mr-2 avatar-sm'>
        //   <img src="/media/${image}" /> 
        //   </figure>`
        //   counter++

        // }
      
        

        $('#output').html("IIIIIIIIIIIIII")
      })
  })







  $('#userSearch').on('keyup', () => {
    let username = $('#userSearch').val()
    if (username.length === 0) {
      $('#searchResult').addClass('visible')
      return
    }
    fetch(`/searchJson/?username=${username}`)
      .then(response => response.json())
      .then(data => {
        $('#searchResult').removeClass('invisible')
        let result = ''
        if (data.length === 0) {
        $('#searchResult').removeClass('card')

          result = `<div class='alert alert-warning alert-dismissible fade show'>
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          <strong>Empty!</strong> No Match for your search.
        </div>`
        $('#searchResult').html(result)
        return
        }
        $('#searchResult').addClass('card')
        for (let d in data) {
          let user = data[d]
result+= ` <div  class=" people-list"  >
<div class="m-b-20">
  <div id="chat-scroll">
    <ul class="chat-list list-unstyled m-b-0">
      
      <a href="/profile/${user[0].id_user}/"> 
        <li class="clearfix">
          <figure class="avatar float-left">
          <img src="${user[1]}" alt="avatar">
        </figure> 
          <div class="about">
            <div class="name">@${user[2]}</div>
            <div class="status">
              
            </div>
          </div>
        </li>
      </a>

    </ul>
  </div>
</div>
</div>`

        }
        $('#searchResult').html(result)
      })
  })

})