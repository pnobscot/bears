from abc import ABC, abstractmethod
from enum import Enum
import random

# # CONSTANTS GO HERE
TEMP = 6 # stealing from others
REWARD = 4 # cooperating with others
PUNISH = 1 # both stealing
SUCKERS = 0 # stolen from
SOLO = 2 # play by yo self

# how many solo games are played after 2 betrayals
NUM_SOLO_GAMES = 3
# how many games are played (solo or normal) in a round
GAMES_PER_ROUND = 10
# likelyhood that a bear will forgive after 2 betrayals
# 1.0 is 100% forgiveness
FORGIVENESS_CHANCE = 0.25



class Strategy(ABC):
    @abstractmethod
    def get_move(self, bear: "Bear", partner_bear_id: int):
        pass

    @abstractmethod
    def update_memory(self, bear: "Bear", partner_bear_id: int):
        pass

    @abstractmethod
    def __str__(self):
        pass
        
class MoveType(Enum):
    EFFORT = 1
    STEAL = 2

class Bear:
    # this is a class variable, shared among all of the bears
    _next_id_: int = 1

    def __init__(self, strategy: Strategy):
        self.id = Bear._next_id_
        self.berries = 0
        self.memory: dict[int, MoveType] = {}
        self.stat_tracker: dict[str, dict[str, int]] = {}
        # model for this ^ is:
        # {'Grim Trigger': {"games": 0, "berries": 0}}
        # {'Eye for An Eye': {"games": 0, "berries": 0}} etc
        self.strategy = strategy
        self.games_played = 0
        self.solo_games_played = 0
        self.times_cooperated = 0
        Bear._next_id_ += 1

    def update(self, partner_bear_id: int):
        # use strategy to update memory
        self.strategy.update_memory(self, partner_bear_id)

    def choose_move(self, partner_bear_id: int):
        # use strategy to choose move
        return self.strategy.get_move(self, partner_bear_id)

    def print_stats(self):
        print(f'Strategy: {self.strategy}')
        print(f'Berries: {self.berries}')
        # memory is mainly for debug
        # print(f'Memory: {self.memory}') 
        print(f'Number of effort choices: {self.times_cooperated}')
        print(f'Solo games played: {self.solo_games_played}')
        # print(f'ID: {self.id}')
        # print(f'Games Played: {self.games_played}')

class AlwaysEffort(Strategy):
    def get_move(self, bear: Bear, partner_bear_id: int):
        return MoveType.EFFORT
    def update_memory(self, bear: Bear, partner_bear_id: int):
        pass
    def __str__(self):
        return 'Always Effort'

class AlwaysSteal(Strategy):
    def get_move(self, bear: Bear, partner_bear_id: int):
        return MoveType.STEAL
    def update_memory(self, bear: Bear, partner_bear_id: int):
        pass
    def __str__(self):
        return 'Always Steal'
    
class Random(Strategy):
    def get_move(self, bear: Bear, partner_bear_id: int):
        options = [MoveType.EFFORT, MoveType.STEAL]
        return random.choice(options)
    def update_memory(self, bear: Bear, partner_bear_id: int):
        pass
    def __str__(self):
        return 'Random'
    
# this strat will start its very first game with effort,
# any games after that come directly from the number of-
# berries gained last round. if we got stolen from on the-
# final game of our previous round, we will shift, 
# making us start the next round stealing
class WinStayLoseShift(Strategy):
    def __init__(self):
        self.berries_last_game = 0
        self.move = MoveType.EFFORT

    def get_move(self, bear: Bear, partner_bear_id: int):
        return self.move

    def switch_move(self):
        # print(f'------current move:{str(self.move)} is being switched--------')
        if self.move == MoveType.EFFORT:
            self.move = MoveType.STEAL
        else:
            self.move = MoveType.EFFORT

    def update_memory(self, bear: Bear, partner_bear_id: int):
        berries_gained = bear.berries - self.berries_last_game

        # if we did not gain 4 or 6 berries, switch move
        if berries_gained < 3:
            self.switch_move()
        self.berries_last_game = bear.berries
    
    def __str__(self):
        return 'Win Stay Lose Shift'
    
# lone wolf strategy
# always triggers solo games
class LoneWolf(Strategy):
    # there are no moves or memory
    # the round will trigger lone wolf stuff
    def get_move(self, bear: Bear, partner_bear_id: int):
        pass
    def update_memory(self, bear: Bear, partner_bear_id: int):
        pass
    def __str__(self):
        return 'Lone Wolf'

# eye for an eye
# if you betray me 1x, I will betray you 1x
# basically copy what the opponent did last round
# when we play that bear again in future rounds,
# we will remember what they did against us
class EyeForEye(Strategy):
    def __init__(self):
        self.berries_last_game = 0

    def get_move(self, bear: Bear, partner_bear_id: int):
        opponent_last_move = bear.memory.get(partner_bear_id)
        if opponent_last_move == None:
            return MoveType.EFFORT
        else:
            return opponent_last_move

    def update_memory(self, bear: Bear, partner_bear_id: int):
        berries_gained = bear.berries - self.berries_last_game
        opponent_last_move = None
        # 4 berries = cooperation, 6 = we stole
        # either way, the opponent did effort, so we copy
        if berries_gained == 4 or berries_gained == 6:
            opponent_last_move = MoveType.EFFORT
        # 0 berries = betrayal, 2 berries = both steal
        # either way, the opponent stole, so we copy
        if berries_gained == 0 or berries_gained == 2:
            opponent_last_move = MoveType.STEAL
        # other amounts of berries come from solo games, 
        # or lone wolf rounds. neither should change strategy
        

        # assign the last move to a bear so we can copy them
        bear.memory[partner_bear_id] = opponent_last_move
        # update memory of berries for future
        self.berries_last_game = bear.berries

    def __str__(self):
        return 'Eye For An Eye'

# grim trigger
# give effort until betrayed, then betray every time
# needs memory of which bear betrayed only
class GrimTrigger(Strategy):
    def __init__(self):
        self.berries_last_game = 0

    def get_move(self, bear: Bear, partner_bear_id: int):
        trigger = bear.memory.get(partner_bear_id)
        if trigger == None:
            return MoveType.EFFORT
        else:
            return trigger

    def update_memory(self, bear: Bear, partner_bear_id: int):
        # if the trigger is not steal it will be None
        # check to see if we got stolen
        if bear.memory.get(partner_bear_id) == None:
            berries_gained = bear.berries - self.berries_last_game
            trigger = None
            # 0 berries = betrayal
            # our trigger will now flip
            if berries_gained == 0:
                trigger = MoveType.STEAL
            # 2, 4, and 6 berries don't matter
            # other amounts of berries come from solo games,
            # or lone wolf rounds. neither should change strategy

            # assign the last move to a bear so we can copy them
            bear.memory[partner_bear_id] = trigger
        
        # if the trigger is not None, it has been flipped, so we keep it that way
        
        # now update memory of berries for future
        self.berries_last_game = bear.berries

    def __str__(self):
        return 'Grim Trigger'

def play_berry_game(b1: Bear, b2: Bear):
    b1move = b1.choose_move(b2.id)
    b2move = b2.choose_move(b1.id)
    name1 = str(b1.strategy)
    name2 = str(b2.strategy)
    thief = None
    b1_berries = 0
    b2_berries = 0

    # cooperation / reward
    if b1move == MoveType.EFFORT and b2move == MoveType.EFFORT:
        b1_berries += 4
        b2_berries += 4
        outcome = name1+' and '+name2+' cooperated!'
        b1.times_cooperated += 1
        b2.times_cooperated += 1
    # both steal / punishment
    elif b1move == MoveType.STEAL and b2move == MoveType.STEAL:
        b1_berries += 2
        b2_berries += 2
        outcome = name1+' and '+name2+' tried to steal from each other.'
    # suckers payoff, bear 2 steals
    elif b1move == MoveType.EFFORT and b2move == MoveType.STEAL:
        b1_berries += 0
        b2_berries += 6
        outcome = name2+' stole from '+name1+'!'
        thief = b2
        b1.times_cooperated += 1
    # suckers payoff, bear 1 steals
    elif b1move == MoveType.STEAL and b2move == MoveType.EFFORT:
        b1_berries += 6
        b2_berries += 0
        outcome = name1+' stole from '+name2+'!'
        thief = b1
        b2.times_cooperated += 1

    # give berries to each bear
    b1.berries += b1_berries
    b2.berries += b2_berries
    # update total game counter
    b1.games_played += 1
    b2.games_played += 1
    # update bear memory
    b1.update(b2.id)
    b2.update(b1.id)

    # update stat tracker
    update_stat_tracker(b1, b2, b1_berries, b2_berries)

    # display game
    # print(f'Game Result: {outcome}')

    # this is used for counting betrayals in rounds
    return thief

def play_solo_games(normal_games_played_this_round: int, b1: Bear, b2: Bear):
    num_solo_games = NUM_SOLO_GAMES
    # defualt nums are 10 games/round, 3 solo rounds
    # it is possible that we play less than 3 so.o if we played 8+ games already
    # 10 games per round - 8 games already played = only 2 games left
    if (GAMES_PER_ROUND - normal_games_played_this_round) < NUM_SOLO_GAMES:
        num_solo_games = (GAMES_PER_ROUND - normal_games_played_this_round)

    solo_games_played = 0
    # give each bear 3 berries until we have played all needed games
    while solo_games_played < num_solo_games:
        # give each bear 3 berries
        b1.berries += 3
        b2.berries += 3
        # count this as a game played
        solo_games_played += 1
    # at this point, we have played the correct amount of solo games

    # update game counter
    b1.games_played += num_solo_games
    b2.games_played += num_solo_games
    b1.solo_games_played += num_solo_games
    b2.solo_games_played += num_solo_games

    # name each bear to print them
    name1 = str(b1.strategy)
    name2 = str(b2.strategy)
    # print(f'{name1} and {name2} gathered berries by themselves for {num_solo_games} rounds.')
    return solo_games_played

def play_round(b1: Bear, b2: Bear):
    # check for lone wolf, go to lone wolf round if so
    if (str(b1.strategy) == 'Lone Wolf') or (str(b2.strategy) == 'Lone Wolf'):
        lone_wolf_round(b1, b2)
        return

    # count how many times each bear steals
    b1_steals = 0
    b2_steals = 0
    # keep track of games played so we loop to correct amount
    games_played = 0

    while games_played < GAMES_PER_ROUND:
        if ((b1_steals == 2) or (b2_steals == 2)) and NUM_SOLO_GAMES > 0:
            # play solo games
            solo_games_played = play_solo_games(games_played, b1, b2)
            games_played += solo_games_played

            # after this part, the solo games have been played
            # if we have played all the games in the round, we should break
            if games_played == GAMES_PER_ROUND:
                break
            
            # if we have not played all of the games in the round, try forgiveness
            forgiveness = random.random() < FORGIVENESS_CHANCE

            # if we didn't forgive, we will skip the normal game below
            # the betrayal count will still be 2, triggering another solo game round
            if not forgiveness:
                continue
            
            # print('---------------FORGIVENESS---------------')
            # forgiveness happened, so we will:
            # 1- reset the betrayal counters
            b1_steals = 0
            b2_steals = 0
            # 2- reset bear memory if GrimTrigger or EyeForEye
            bears_forgive(b1, b2)

            # 3- resume play game loop as normal
            # this happens below :)

        theif = play_berry_game(b1, b2)
        games_played += 1

        if theif != None:
            if theif == b1:
                b1_steals += 1
                # print('_-------------------BEAR 1 STOLE---------------') 
                # print(b1_steals)
            if theif == b2:
                b2_steals += 1
                # print('_-------------------BEAR 2 STOLE---------------') 
                # print(b2_steals)

    # print(f'gamed played this round: {games_played}')

# playing with lone wolf does not change your strategy at all
def lone_wolf_round(b1: Bear, b2: Bear):
    # give each bear berries
    berries_to_collect = 3 * GAMES_PER_ROUND
    b1.berries += berries_to_collect
    b2.berries += berries_to_collect

     # name each bear to print them
    name1 = str(b1.strategy)
    name2 = str(b2.strategy)
    # print(f'{name1} and {name2} gathered berries by themselves for {GAMES_PER_ROUND} rounds.')

    # update game counter
    b1.games_played += GAMES_PER_ROUND
    b2.games_played += GAMES_PER_ROUND
    b1.solo_games_played += GAMES_PER_ROUND
    b2.solo_games_played += GAMES_PER_ROUND
    
    # skip the update step, because there really was no interaction. 
    # playing with lone wolf does not change your strategy at all

# some strats have specific forgiveness needs
def bears_forgive(b1: Bear, b2: Bear):
    # grim trigger deletes steal trigger b1
    if str(b1.strategy) == 'Grim Trigger':
        # make sure our berries counter is up to current
        b1.strategy.berries_last_game = b1.berries
        # check to make sure we had a move there
        trigger = b1.memory.get(b2.id)
        # print error if we did not
        if trigger == None:
            print('Weird error. There should have been a MoveType.STEAL in there')
        # now get rid of previous move to reset / forgive
        del b1.memory[b2.id]
    
    # copy for b2
    if str(b2.strategy) == 'Grim Trigger':
        # make sure our berries counter is up to current
        b2.strategy.berries_last_game = b2.berries
        # check to make sure we had a move there
        trigger = b2.memory.get(b1.id)
        # print error if we did not
        if trigger == None:
            print('Weird error. There should have been a MoveType.STEAL in there')
        # now get rid of previous move to reset / forgive
        # print('------------MEMORY DELETED---------------')
        del b2.memory[b1.id]

    # reset eye for eye b1
    if str(b1.strategy) == 'Eye For An Eye':
        # make sure our berries counter is up to current
        b1.strategy.berries_last_game = b1.berries
        # check to make sure we had a move there
        move = b1.memory.get(b2.id)
        # print error if we did not
        if move == None:
            print('Weird error. There should have been a move there')
        # now get rid of previous move to reset / forgive
        # print('------------MEMORY DELETED---------------')
        del b1.memory[b2.id]

    # repeat for bear 2
    if str(b2.strategy) == 'Eye For An Eye':
        # make sure our berries counter is up to current
        b2.strategy.berries_last_game = b2.berries
        # check to make sure we had a move there
        move = b2.memory.get(b1.id)
        # print error if we did not
        if move == None:
            print('Weird error. There should have been a move there')
        # now get rid of previous move to reset / forgive
        del b2.memory[b1.id]

    # wsls for bear 1
    if str(b1.strategy) == 'Win Stay Lose Shift':
        move = b1.strategy.get_move(b1, b2.id)
        if move == MoveType.STEAL:
            b1.strategy.switch_move()
    # repeat for bear 2
    if str(b2.strategy) == 'Win Stay Lose Shift':
        move = b2.strategy.get_move(b2, b1.id)
        if move == MoveType.STEAL:
            b2.strategy.switch_move()

def update_stat_tracker(b1: Bear, b2: Bear, b1_b: int, b2_b: int):
    # strategy names are keys for tracker dict
    s1 = str(b1.strategy)
    s2 = str(b2.strategy)

    # ensure b1 has a key for b2's strategy
    if s2 not in b1.stat_tracker:
        b1.stat_tracker[s2] = {"games": 0, "berries": 0}

    # ensure b2 has a key for b1's strategy
    if s1 not in b2.stat_tracker:
        b2.stat_tracker[s1] = {"games": 0, "berries": 0}

    # update b1's stats
    b1.stat_tracker[s2]["games"] += 1
    b1.stat_tracker[s2]["berries"] += b1_b

    # now b2
    b2.stat_tracker[s1]["games"] += 1
    b2.stat_tracker[s1]["berries"] += b2_b


def spawn_bears_for_strat(num_bears: int, strat_class: type[Strategy]):
    bears = []
    for _ in range(num_bears):
        bear = Bear(strat_class())
        bears.append(bear)
    return bears

def create_bear_generation(num_effort, num_steal, num_random, num_wsls, num_wolf, num_eye, num_grim):
    bears = []
    bears.extend(spawn_bears_for_strat(num_effort, AlwaysEffort))
    bears.extend(spawn_bears_for_strat(num_steal, AlwaysSteal))
    bears.extend(spawn_bears_for_strat(num_random, Random))
    bears.extend(spawn_bears_for_strat(num_wsls, WinStayLoseShift))
    bears.extend(spawn_bears_for_strat(num_wolf, LoneWolf))
    bears.extend(spawn_bears_for_strat(num_eye, EyeForEye))
    bears.extend(spawn_bears_for_strat(num_grim, GrimTrigger))
    return bears

# in a season, all of the bears play each other (each pair plays once)
def play_season(bears: list[Bear]):
    # get the total number of bears
    num_bears = len(bears)

    # outer loop: choose the first bear by index
    # i goes from 0 up to the second-to-last bear
    for i in range(num_bears):

        # inner loop: choose the second bear
        # j starts at i + 1 so:
        #   - we never match a bear with itself
        #   - we never repeat a matchup (B vs A after A vs B)
        for j in range(i + 1, num_bears):

            # play one round between these two unique bears
            play_round(bears[i], bears[j])


def print_stats_for_bears(bears: list[Bear]):
    for bear in bears:
        bear.print_stats()

def collect_total_berries_and_bpg_per_strat(bears: list[Bear]):
    effort_berries = 0
    steal_berries = 0
    random_berries = 0
    wsls_berries = 0
    wolf_berries = 0
    eye_berries = 0
    grim_berries = 0

    for bear in bears:
        if isinstance(bear.strategy, AlwaysEffort):
            effort_berries += bear.berries
        elif isinstance(bear.strategy, AlwaysSteal):
            steal_berries += bear.berries
        elif isinstance(bear.strategy, Random):
            random_berries += bear.berries
        elif isinstance(bear.strategy, WinStayLoseShift):
            wsls_berries += bear.berries
        elif isinstance(bear.strategy, LoneWolf):
            wolf_berries += bear.berries
        elif isinstance(bear.strategy, EyeForEye):
            eye_berries += bear.berries
        elif isinstance(bear.strategy, GrimTrigger):
            grim_berries += bear.berries
    return effort_berries, steal_berries, random_berries, wsls_berries, wolf_berries, eye_berries, grim_berries

def main():
    kenai = Bear(AlwaysSteal())
    nice = Bear(AlwaysEffort())
    wolf = Bear(LoneWolf())

    play_round(nice, wolf)
    nice.print_stats()

if __name__ == "__main__":
    main()

# 50 bears are made of each different strat
# bears play all other bears
# these bears play 10 games in a round, in the same bear pairing
# this ^ is 1 season, we repeat this for several seasons 
# if bears are stolen from twice, they play solo games
# bears can forgive (% chance) after solo games to resume normal games

#TODO: evolution????


  