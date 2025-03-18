$(document).ready(() => {
  const followBtnClass = 'btn btn-primary'
  const unfollowBtnClass = 'btn btn-dark'

  $('#followBtn').click(() => {
    const userId = $('#userId').attr('value')

    fetch(`/follow/?followed_id=${userId}`)
      .then(response => response.json())
      .then(data => {
        const isFollowed = data['is_followed']
        $('#followBtn').attr('class', isFollowed ? unfollowBtnClass : followBtnClass)
          .html(isFollowed ? '- Unfollow' : '+ Follow')
        $('#followersCount').html(data['followers'].length)
        $('#followingCount').html(data['following'].length)

      })
  })
}) 
