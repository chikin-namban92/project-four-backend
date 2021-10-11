# Find Floppas
SEI Project Four

# Overview
Find Floppas is a dating app parody heavily inspired by the likes of Tinder and Bumble. I chose to build this project entirely solo as I wanted a greater opportunity to work with frontend technologies that I missed out a bit on in Project 3. My main goal for the app was to create a working user to user matching and messaging function as seen in other dating apps.
![Screenshot 2021-10-12 at 00 03 04](https://user-images.githubusercontent.com/71222270/136865252-1c14f292-372d-4364-aa4d-4d48ae442f3f.png)

# Brief
This task was largely similar to Project Three in the sense we were required to build a full stack web app from scratch within seven days. As with Project Three our app had to be a complete product with CRUD functionality, consume our own API using a React frontend and be deployed online. The key difference this time was to build the backend using a Python Django API with Django REST Framework serving the data from a Postgres database.

# Link
https://find-floppas.netlify.app/
Feel free to login with the following credentials to test out the site:
* Username - `testuser`
* Password - `testpassword`

# Instructions
* Clone or download both the frontend and the backend to the same directory.
* Install backend dependencies with `pipenv install`.
* Enter shell for the project with `pipenv shell`.
* Make migrations by entering `python manage.py makemigrations`.
* Finalise migrations: `python manage.py migrate`.
* Load user seed data with `python manage.py loaddata jwt_auth/seeds.json`.
* Initiate the server with `python manage.py runserver`.
* Change to the frontend directory named ‘client’ and install dependencies with `npm i`.
* Start the frontend server with `npm run dev`.

# Technologies
### Backend ###
* Python
* Django
* Django REST Framework
* PostgreSQL
* pyJWT

### Frontend ###
* React
* Axios
* SCSS
* Bulma
* Nodemon
* React Router Dom
* React Chat Elements
* React Alice Carousel

### Development Tools ###
* VS Code
* npm / pip
* Insomnia
* Git / GitHub
* Firefox Developer Edition
* Heroku
* Netlify

# Process
As this was a solo project and I already had a clear idea I wanted to create a dating app parody with messaging functionality I was able to get to work immediately on creating my wireframes for the frontend layout. Due to the higher level of required planning to create a Django backend I also created an ERD diagram to get a clear idea on how to set up my models before I started coding.
![Screenshot 2021-10-11 at 23 55 40](https://user-images.githubusercontent.com/71222270/136864772-c49cb27d-db48-494b-b556-49f6ca6d5fda.png)
Despite this being a solo project I wanted to keep up good practices so I ensured I regularly pushed to my GitHub repository and used branches to keep my code in order when working on a new feature. 

### Backend ###
As this was my first experience being a backend in Python using Django I did struggle at first to get my head around the datatables. Unlike in my Express API from the previous project it proved a lot more time consuming to alter my models and reset the database so I wanted to ensure I got things correct early on. I ended up creating three models, the User, the Chat which matched users are automatically added to, and the Message. 

After my initial headaches getting to grips with Django I was able to successfully create a PostgreSQL database with RESTful functionality. The user can register and login, as well as send messages and like / unlike other user’s profiles. To test the data and JSON responses I used Insomnia to ensure the RESTful functionality and authorisation features were all working correctly.
```
class MessagePostView(APIView):
   ''' List / Create View for Messages '''
 
   permission_classes = (IsAuthenticated, )
 
   def post(self, request, chat_pk):
       request.data['parent_chat'] = chat_pk
       request.data['sender'] = request.user.id
       created_message = MessageSerializer(data=request.data)
       if created_message.is_valid():
           created_message.save()
           return Response(created_message.data, status=status.HTTP_201_CREATED)
       return Response(
           created_message.errors,
           status=status.HTTP_422_UNPROCESSABLE_ENTITY
           )
```
```
class UserLikeView(APIView):
   ''' Adds user to liked_users and vice versa and removes if already liked '''
   permission_classes = (IsAuthenticated, )
 
   def post(self, request, user_pk):
       try:
           user_to_like = User.objects.get(pk=user_pk)
       except User.DoesNotExist:
           raise NotFound()
 
       if request.user in user_to_like.liked_by.all():
           user_to_like.liked_by.remove(request.user.id)
       else:
           user_to_like.liked_by.add(request.user.id)
 
       if (
           request.user in user_to_like.liked_by.all()
           ) and (
               request.user in user_to_like.liked_users.all()
               ):
           chat_to_create = Chat.objects.create()
           chat_to_create.matched_users.add(request.user.id, user_to_like)
 
       return Response(status=status.HTTP_202_ACCEPTED)
```
### Frontend ###
As I wanted to use this project largely as an exercise in getting user to user messaging functionality in place, I decided to keep the styling quite simple. I used Bulma as I was already quite comfortable with it, and React to allow seamless navigation around the site. Once again I implemented Axios to communicate with the backend which worked smoothly as I’d done thorough testing when building the back end.

Once the user is registered and logged in they have the ability to navigate to the users index page to begin liking other profiles. This is placed behind a secure route so if an unauthorised user tries to access a restricted page via the url they are redirected to the login page.
```
function SecureRoute({ component: Component, ...rest }) {
 if (isAuthenticated()) return <Route {...rest} component={Component} />
 removeToken()
 return <Redirect to="/auth/login" />
}
```
The user index page displays each profile as a card with the users information and a like and dislike button. Currently the dislike button doesn’t have any functionality as I struggled with hiding the cards from only the current user. Instead it was hiding for every subsequent user that would log in. The like button adds the target profile to the current user’s liked users array. During this process a check is performed in the backend code to create a new chat with the two users if they have now liked each other.

```
const handleLike = async (e) => {
   const likedUserId = e.target.parentElement.id
   console.log(likedUserId)
   try {
     const like = await likeUser(likedUserId)
     return true
   } catch (err) {
     console.log(err)
   }
 }
```
My biggest win in the whole project was setting up a working and responsive messaging feature. This was a big challenge, setting it up how a user would expect with sender and receiver messages appearing distinct, the chat starting from the earliest message on load and the message list updating as soon as a new message is posted. I decided to use React Chat Elements (linked above) as it had the functionality I was looking for and the potential to add further UX features such as notifications etc.

Once I accessed the chat list I had to discern which chats the user was authorised to see. At first I ran into an issue where the user would see every chat but only the messages from a single user. To fix this I implemented the following code to return nothing if the current user is not found in the chat’s matched users array
```
const isCurrentUser = () => {
   if (isOwner(chat.matchedUsers[0].id)) {
     return chat
   } else if (isOwner(chat.matchedUsers[1].id)) {
     return chat
   }
   return
 }
```
Another big hurdle I had was what to display in the text preview if there were no existing messages between users. I decided I wanted to display a message encouraging the users to start a conversation, much like what is found on other dating apps. I realised the best way to go about this was to perfect a boolean check for a falsey value at array position 0. For the opposite I wanted to display the most recent message as a preview hence the array.length - 1.
```
const textDisplay = () => {
   if (!chat.messagesInChat[0]) {
     return `Start your conversation with ${isLoggedInUser()}`
   } else if (chat.messagesInChat[chat.messagesInChat.length - 1].text) {
     return chat.messagesInChat[chat.messagesInChat.length - 1].text
   }
 }
```
![Screenshot 2021-10-12 at 00 00 02](https://user-images.githubusercontent.com/71222270/136865060-06a9c570-d06a-43c9-a01d-e4e395e4db85.png)
# Wins
* My biggest win was getting the chat functionality working as expected. Whilst there are still a few UX issues to iron out (i.e. the notifications) the core functionality is up and running and communicates with the backend while displaying the correct messages and chats.
* Going from zero Python knowledge to building an entire backend in just over a week was something I’m very pleased with and has shown me that adapting to different technologies is not as daunting as it seems at first.
* The user matching functionality is working which was another hurdle I was keen to overcome.

# Challenges
* Having the user profile cards appear as a deck in a similar manner to Tinder was a struggle. They are currently just displayed as a list which works but doesn’t look as good as I’d hoped.
* Having the cards disappear for just the user that liked or disliked them was also difficult. My initial code removed them for every user of the site so this is something I’d like to go back to at a later date.

# Improvements
* I’d like to finish off the styling across the website such as improving the look of the user cards.
* Get the new message notification functionality working correctly.
* Loading spinners.
* I originally thought about filter functionality to only show profiles with similar interests and location to the user. This was not possible with the time frame involved but definitely something to consider.
* Add an unmatch button on the chat pages. This would just be the same as the like button as the functionality is in place to act like a toggle already.

# Key Learnings
As our final project at General Assembly I was really blown away with how much I’d been able to learn. I was a bit apprehensive at first using Python for the backend as I’d had no experience with it prior to this project. Despite a few headaches early on with the data models I was able to adapt very quickly to a new library of tools. 

I’ve also now gained a good understanding on how to set up basic messaging functionality which was my main goal for the project. We hadn’t specifically covered this in our studies so I was extremely pleased with how it turned out!
