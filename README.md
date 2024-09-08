### Music Recommender

## Description

This Music Recommendation System is part of a project for CSUF's CPSC 481 Artificial Intelligence course in which we were tasked with building our own, simple, Artificial Intelligence system.

I initially built this in 2020, but I revisted it in late 2024 to re-organize and remove some old clutter.

## Inspiration and Motivation

The motivation for this project is from my personal interest in both Music and Artificial Intelligence. Recommendation systems are implemented in various ways across various fields of research and industries. I was interested in how these systems were created, and following that interest led me to a paper written by [Òscar Celmai](http://www.ocelma.net/) titled [Music Recommendation and Discovery in the Long Tail](http://ocelma.net/MusicRecommendationBook/index.html) in which they describe the work behind building comprehensive music recommendation systems among other informative concepts.

## Goal

Utilize a simple form of [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering) in which an existing context will be provided by the user and a new set of recommendations is constructed based off of candidates from a set of collaborative contexts, where these contexts are stored and fetched from an arbitrary storage medium/context.

## Implementation

In our case, a collaborative context will be a playlist, and we will consider a collaborative context more or less similar to a user-provided context depending on how many songs they share. In other words, the more songs shared between a user-provided playlist and some arbitrary playlist from storage, the more similar they will be considered and the more the arbitrary playlist will be sampled for song candidates.

## Requirements
- Python 3

## Usage

### Receive a recommendation
```sh
python main.py [SOURCE_LINK | SAVED_CANDIDATE_ID]
```
For the scope of the project, I chose to only support YouTube as a source to reduce initial complexity (this is a proof of concept afterall). As such, `SOURCE_LINK` would be a link to a playlist of the form
`https://www.youtube.com/playlist?list=<PLAYLIST_ID>` and `SAVED_CANDIDATE_ID` is the `PLAYLIST_ID` if it has been processed before.


### Seed the collaborative pool

Playlists entered by the user are saved in order to grow the pool of candidate playlists for future executions of the recommendation system (see [cold starts](https://en.wikipedia.org/wiki/Cold_start_(recommender_systems))) as to why. If you wish to pre-emptively seed the pool with more candidates to start with, run the following if you're on macOS or Linux.

```sh
./pool.sh
```

or the following if you're on Windows

```
./pool.bat
```

This will pre-populate the pool with a preset of 43 playlists. It's not entirely likely that you will have these songs in the playlist you provide, but it's good for testing.
