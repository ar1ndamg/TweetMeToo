import React, { useEffect, useState } from 'react';
import { loadTweets } from '../lookup'

export function TweetComponent(props) {
  const textareaRef = React.createRef()
  const [newTweets, setNewTweets] = useState([])
  const handleSubmit = (event) => {
    event.preventDefault()
    const newContent = textareaRef.current.value
    let tmpTweets = [...newTweets]
    tmpTweets.unshift({
      content: newContent,
      id: 123,
      likes: 0
    })
    setNewTweets(tmpTweets)
    textareaRef.current.value = ""
  }
  return <div className={props.className}>
    <div className="col-10 mb-3 pt-3 mt-5 mx-auto">
      <form onSubmit={handleSubmit}>
        <textarea ref={textareaRef} required={true} className="form-control" name="tweet">
        </textarea>
        <button className="btn btn-primary my-3" type="submit">Tweet</button>
      </form>
    </div>
    <TweetsList newTweets={newTweets}/>
  </div>
}

export function TweetsList(props) {
  const [tweetsInit, setTweetsInit] = useState([])
  const [tweets, setTweets] = useState([])
  
  useEffect(() => {
    const final = [...props.newTweets].concat(tweetsInit)
    if (final.length !== tweets.length){
      setTweets(final)
    }
  }, [props.newTweets, tweetsInit, tweets])

  useEffect(() => {
    const myCallback = (response, status) => {
      if (status === 200) {
        setTweetsInit(response);
      }
      else {
        alert(response.message)
      }
    }
    loadTweets(myCallback);
  }, []);
  return tweets.map((item, index) => {
    return <Tweet tweet={item} key={`${index}-tweet-${item.id}`} className="my-5 py-5 border bg-white text-dark" />
  })
}

export function ActionBtn(props) {
  const { tweet, action } = props
  const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0);
  const [userLiked, setUserLiked] = useState(tweet.userLiked ? true : false);
  const actionDisplay = action.display ? action.display : "Action"
  const display = action.type === "like" ? `${likes} ${actionDisplay}` : actionDisplay
  const className = props.className ? props.className : "btn btn-primary btn-sm";
  const handleClick = (event) => {
    event.preventDefault()
    if (action.type === "like") {
      if (!userLiked) {
        setLikes(likes + 1)
        setUserLiked(true)
      }
      else {
        setLikes(likes - 1)
        setUserLiked(false)
      }
    }
  }
  return <button className={className} onClick={handleClick}>{display}</button>
}

export function Tweet(props) {
  const { tweet } = props
  const className = props.className ? props.className : "col-12 col-md-10 rounded mx-auto border py-3 mb-4 tweet";
  return <div className={className}>
    <p>{tweet.id} - {tweet.content}</p>
    <div className="btn btn-group">
      <ActionBtn tweet={tweet} action={{ type: "like", display: "Likes" }} />
      <ActionBtn tweet={tweet} action={{ type: "unlike", display: "Unlike" }} />
      <ActionBtn tweet={tweet} action={{ type: "retweet", display: "Retweets" }} />
    </div>
  </div>
}