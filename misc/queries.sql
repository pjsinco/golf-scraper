create table player (
  `f_name`
  `l_name`
  `birthplace`
  `college`
  `dob`
  `swings`
  `pga_debut`
  `l_name`
)

create table tournament (
  `id`
  `name`
  `year`
  `purse`
)

create table plays_round (
  `player_id` 
  `tourn_id`
  `round`
  `par`
)

create table plays_tournament (
  `player_id`
  `tourn_id`
  `earnings`
  `to_par`
  
)

# http://espn.go.com/golf/leaderboard11/controllers/ajax/playerDropdown?xhr=1&playerId=308&tournamentId=119
