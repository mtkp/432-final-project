432-final-project
=================

432 Final Project - [Network Game](https://canvas.uw.edu/courses/895740/assignments/2435056)

Game server port: `7307`

### Links
##### Game Dev
- [Game Programming Patterns](http://gameprogrammingpatterns.com/)
- [Writing Games - sjbrown](http://ezide.com/games/writing-games.html)
  - [Sample code](https://github.com/sjbrown/writing_games_tutorial)

##### Backend
- [Python socket library](https://docs.python.org/2/library/socket.html)
- [Python sockets HOWTO](https://docs.python.org/2/howto/sockets.html#socket-howto)
- [Python thread library](https://docs.python.org/2/library/threading.html)
- [Threading tutorial](http://www.tutorialspoint.com/python/python_multithreading.htm)

##### Frontend
- [Pygame](http://www.pygame.org/news.html)
- [Pygame's own tutorial](http://www.pygame.org/docs/tut/tom/MakeGames.html)
- [Program Arcade Games tutorial](http://programarcadegames.com)

##### Misc.
- [Setting up ssh for GitHub (Linux/Mac)](https://help.github.com/articles/generating-ssh-keys) (or just use Windows & the GitHub app)
- [Packaging python apps](https://www.digitalocean.com/community/articles/how-to-package-and-distribute-python-applications)

---

### Using `git`

``` sh
$ git status
$ git add .
$ git commit -m "my commit msg"
$ git push
```
##### A little bit more detail

1. (optional) Pull previous commits from remote: `git pull`
2. Check status: `git status`
3. Add changes: `git add my_file.py other_file.py`
  - or commit all changes in *current directory* with: `git add .`  
  - or commit all changes in *entire project* with: `git add :/`
4. Check status again to make sure everything is added: `git status`
5. Commit added changes: `git commit` or `git commit -m "my commit msg"`
6. (optional) Push to remote: `git push origin master` or `git push`
  - might need to `git pull` first
