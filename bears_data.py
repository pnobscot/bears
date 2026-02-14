import bnb
from tabulate import tabulate

def percent_coop(effort_choices, games_played, solo_games_played):
    normal_games = games_played - solo_games_played
    if normal_games > 0:
        percent_coop = effort_choices / normal_games
        return percent_coop
    else:
        return 0

def collect_data(bears: list[bnb.Bear], num_seasons, num_strat):
    gen_berries = 0
    gen_games = 0
    gen_solo_games = 0
    gen_c_choices = 0

    effort_berries = 0
    steal_berries = 0
    random_berries = 0
    wsls_berries = 0
    wolf_berries = 0
    eye_berries = 0
    grim_berries = 0

    effort_games = 0
    steal_games = 0
    random_games = 0
    wsls_games = 0
    wolf_games = 0
    eye_games = 0
    grim_games = 0

    effort_c_choices = 0
    steal_c_choices = 0
    random_c_choices = 0
    wsls_c_choices = 0
    wolf_c_choices = 0
    eye_c_choices = 0
    grim_c_choices = 0

    effort_solo_games = 0
    steal_solo_games = 0
    random_solo_games = 0
    wsls_solo_games = 0
    wolf_solo_games = 0
    eye_solo_games = 0
    grim_solo_games = 0
    

    for bear in bears:
        if isinstance(bear.strategy, bnb.AlwaysEffort):
            effort_berries += bear.berries
            effort_games += bear.games_played
            effort_c_choices += bear.times_cooperated
            effort_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated
        elif isinstance(bear.strategy, bnb.AlwaysSteal):
            steal_berries += bear.berries
            steal_games += bear.games_played
            steal_c_choices += bear.times_cooperated
            steal_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated
        elif isinstance(bear.strategy, bnb.Random):
            random_berries += bear.berries
            random_games += bear.games_played
            random_c_choices += bear.times_cooperated
            random_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated
        elif isinstance(bear.strategy, bnb.WinStayLoseShift):
            wsls_berries += bear.berries
            wsls_games += bear.games_played
            wsls_c_choices += bear.times_cooperated
            wsls_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated
        elif isinstance(bear.strategy, bnb.LoneWolf):
            wolf_berries += bear.berries
            wolf_games += bear.games_played
            wolf_c_choices += bear.times_cooperated
            wolf_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated
        elif isinstance(bear.strategy, bnb.EyeForEye):
            eye_berries += bear.berries
            eye_games += bear.games_played
            eye_c_choices += bear.times_cooperated
            eye_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated
        elif isinstance(bear.strategy, bnb.GrimTrigger):
            grim_berries += bear.berries
            grim_games += bear.games_played
            grim_c_choices += bear.times_cooperated
            grim_solo_games += bear.solo_games_played
            gen_solo_games += bear.solo_games_played
            gen_games += bear.games_played
            gen_berries += bear.berries
            gen_c_choices += bear.times_cooperated

    eff_bpng  = (effort_berries - (3 * effort_solo_games)) / (effort_games - effort_solo_games) if (effort_games - effort_solo_games) else 0
    ste_bpng  = (steal_berries - (3 * steal_solo_games)) / (steal_games - steal_solo_games) if (steal_games - steal_solo_games) else 0
    ran_bpng  = (random_berries - (3 * random_solo_games)) / (random_games - random_solo_games) if (random_games - random_solo_games) else 0
    wsls_bpng = (wsls_berries - (3 * wsls_solo_games)) / (wsls_games - wsls_solo_games) if (wsls_games - wsls_solo_games) else 0
    wolf_bpng = (wolf_berries - (3 * wolf_solo_games)) / (wolf_games - wolf_solo_games) if (wolf_games - wolf_solo_games) else 0
    eye_bpng  = (eye_berries - (3 * eye_solo_games)) / (eye_games - eye_solo_games) if (eye_games - eye_solo_games) else 0
    grim_bpng = (grim_berries - (3 * grim_solo_games)) / (grim_games - grim_solo_games) if (grim_games - grim_solo_games) else 0

    eff_bpg  = effort_berries / effort_games if effort_games else 0
    ste_bpg  = steal_berries / steal_games if steal_games else 0
    ran_bpg  = random_berries / random_games if random_games else 0
    wsls_bpg = wsls_berries / wsls_games if wsls_games else 0
    wolf_bpg = wolf_berries / wolf_games if wolf_games else 0
    eye_bpg  = eye_berries / eye_games if eye_games else 0
    grim_bpg = grim_berries / grim_games if grim_games else 0

    eff_bpr  = effort_berries * bnb.GAMES_PER_ROUND / effort_games if effort_games else 0
    ste_bpr  = steal_berries * bnb.GAMES_PER_ROUND / steal_games if steal_games else 0
    ran_bpr  = random_berries * bnb.GAMES_PER_ROUND / random_games if random_games else 0
    wsls_bpr = wsls_berries * bnb.GAMES_PER_ROUND / wsls_games if wsls_games else 0
    wolf_bpr = wolf_berries * bnb.GAMES_PER_ROUND / wolf_games if wolf_games else 0
    eye_bpr  = eye_berries * bnb.GAMES_PER_ROUND / eye_games if eye_games else 0
    grim_bpr = grim_berries * bnb.GAMES_PER_ROUND / grim_games if grim_games else 0

    eff_pc  = percent_coop(effort_c_choices, effort_games, effort_solo_games)
    ste_pc  = percent_coop(steal_c_choices, steal_games, steal_solo_games)
    ran_pc  = percent_coop(random_c_choices, random_games, random_solo_games)
    wsls_pc = percent_coop(wsls_c_choices, wsls_games, wsls_solo_games)
    wolf_pc = percent_coop(wolf_c_choices, wolf_games, wolf_solo_games)
    eye_pc  = percent_coop(eye_c_choices, eye_games, eye_solo_games)
    grim_pc = percent_coop(grim_c_choices, grim_games, grim_solo_games)

    gen_bpng = (gen_berries - (3 * gen_solo_games)) / (gen_games - gen_solo_games)
    gen_bpg = gen_berries / gen_games
    gen_bpr = gen_berries / (gen_games / bnb.GAMES_PER_ROUND)
    gen_pc = percent_coop(gen_c_choices, gen_games, gen_solo_games)
    


    return (
        (effort_berries, eff_bpg, eff_bpng, eff_bpr, effort_solo_games, eff_pc),
        (steal_berries, ste_bpg, ste_bpng, ste_bpr, steal_solo_games, ste_pc),
        (random_berries, ran_bpg, ran_bpng, ran_bpr, random_solo_games, ran_pc),
        (wsls_berries, wsls_bpg, wsls_bpng, wsls_bpr, wsls_solo_games, wsls_pc),
        (wolf_berries, wolf_bpg, wolf_bpng, wolf_bpr, wolf_solo_games, wolf_pc),
        (eye_berries, eye_bpg, eye_bpng, eye_bpr, eye_solo_games, eye_pc),
        (grim_berries, grim_bpg, grim_bpng, grim_bpr, grim_solo_games, grim_pc),
        # now we include the generation data
        (gen_berries, gen_bpg, gen_bpng, gen_bpr, gen_solo_games, gen_pc)
        
    )

def format_with_commas(num):
    if isinstance(num, int):
        return f"{num:,}"
    elif isinstance(num, float):
        return f"{num:,.2f}"
    else:
        return num

def print_results_overall(eff, ste, ran, wsls, wolf, eye, grim, gen):
    filename="bear_results_overall.txt"

    rows = [
        ["Always Effort", eff[0], eff[1], eff[2], eff[3], eff[4], eff[5]],
        ["Always Steal", ste[0], ste[1], ste[2], ste[3], ste[4], ste[5]],
        ["Random", ran[0], ran[1], ran[2], ran[3], ran[4], ran[5]],
        ["Win Stay Lose Shift", wsls[0], wsls[1], wsls[2], wsls[3], wsls[4], wsls[5]],
        ["Lone Wolf", wolf[0], wolf[1], wolf[2], wolf[3], wolf[4], wolf[5]],
        ["Eye For An Eye", eye[0], eye[1], eye[2], eye[3], eye[4], eye[5]],
        ["Grim Trigger", grim[0], grim[1], grim[2], grim[3], grim[4], grim[5]],
    ]
    
    # this sorts on the 2nd index which is bpg
    rows.sort(key = lambda x: x[2], reverse = True) 

    gen_row = ["Generation", gen[0], gen[1], gen[2], gen[3], gen[4], gen[5]]
    rows.append(gen_row)

    # add commas to numbers:
    formatted_rows = []
    for row in rows:
        formatted_row = []
        for element in row:
            f_element = format_with_commas(element)
            formatted_row.append(f_element)
        formatted_rows.append(formatted_row)
    
    rows = formatted_rows

    extra = '(' + str(bnb.GAMES_PER_ROUND) + ')'
    table_str = tabulate(
        rows,
        headers=["Strategy", 
                 "Total \nBerries", 
                 "Berries \nper Game", 
                 "Berries per \nNormal Game",
                 "Berries \nper Round " + extra, 
                 "Solo \nGames Played", 
                 "Percent \nEffort Choices"],
        tablefmt="rounded_grid"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(table_str + "\n")   

# ai wrote this puppy because i was feeling lazy
def print_head_to_head_bpg(bears: list[bnb.Bear]):
    filename="bear_head_to_head.txt"

    strategies = [
        "Always Effort",
        "Always Steal",
        "Random",
        "Win Stay Lose Shift",
        "Eye For An Eye",
        "Grim Trigger",
    ]

    stats = {}
    for strategy in strategies:
        stats[strategy] = {}
        for opponent in strategies:
            stats[strategy][opponent] = {"games": 0, "berries": 0}

    for bear in bears:
        bear_strategy = str(bear.strategy)
        if bear_strategy not in strategies:
            continue
        for opponent_strategy, data in bear.stat_tracker.items():
            if opponent_strategy not in strategies:
                continue
            stats[bear_strategy][opponent_strategy]["games"] += data["games"]
            stats[bear_strategy][opponent_strategy]["berries"] += data["berries"]

    # write everything to file
    with open(filename, "w", encoding="utf-8") as f:
        for strategy in strategies:
            rows = []
            for opponent in strategies:
                games_played = stats[strategy][opponent]["games"]
                berries_gained = stats[strategy][opponent]["berries"]
                if games_played > 0:
                    berries_per_game = berries_gained / games_played
                    bpg_display = f"{berries_per_game:.3f}"
                else:
                    bpg_display = "N/A"
                rows.append([opponent, games_played, bpg_display])

            f.write(f"\nAverage Berries Per Game — {strategy} vs Other Strategies\n")
            table_str = tabulate(
                rows,
                headers=["Opponent Strategy", "Normal Games Played", "Berries per Game"],
                tablefmt="rounded_grid"
            )
            f.write(table_str + "\n")

def play_lifetime(num_seasons: int, bears: list[bnb.Bear]):
    for i in range(num_seasons):
        bnb.play_season(bears)

# num strat is how many bears of each strat we want
def avg_bp_lifetime(num_seasons, num_iterations, num_strat): # lifetime is several seasons

    # count berries per lifetime, for society
    total_berries_across_many_lifetimes = 0
    # now count them for each bear
    total_bpg_for_gen_across_many_lifetimes = 0

    for i in range(num_iterations):
        # make a new generation, 20 of each type
        bears = create_equal_generation(num_strat)
        # play 3 seasons
        play_lifetime(num_seasons, bears)
        # get the data
        _, _, _, _, _, _, _, gen = collect_data(bears, num_seasons, num_strat)
        # name the data
        generation_berries_after_one_lifetime = gen[0]
        avg_berries_per_game_for_entire_gen = gen[1]

        # add to current averages
        total_berries_across_many_lifetimes += generation_berries_after_one_lifetime
        total_bpg_for_gen_across_many_lifetimes += avg_berries_per_game_for_entire_gen

    # average number of berries for generation across many lifetimes / iterations:
    avg_berries_per_gen_across_lifetimes = total_berries_across_many_lifetimes / num_iterations
    # average berries per game per bear across many lifetimes / iterations:
    avg_bpg_per_bear_across_lifetimes = total_bpg_for_gen_across_many_lifetimes / num_iterations

    # generational av, then av ber pear
    return avg_berries_per_gen_across_lifetimes, avg_bpg_per_bear_across_lifetimes

def find_best_society(num_seasons, num_strat):
    # start with 0 forgiveness chance
    bnb.FORGIVENESS_CHANCE = 0
    # start best generation tracker
    most_berries = 0
    best_forgiveness = 0
    bpg = 0
    # loop through and test forgiveness
    for i in range(101):

        # now set/increment the forgiveness by .01
        # forgiveness = index / 100: i = 0 gives 0/100 = .00    ->
        # forgiveness = index / 100: i = 1 gives 1/100 = .01
        bnb.FORGIVENESS_CHANCE = i/100

        # for 10 trials, what is the average bpgen on this forgiveness level?
        avg_gen, avg_bear = avg_bp_lifetime(num_seasons, 10, num_strat)

        # debug
        print(f'Forgivness level being tested: {bnb.FORGIVENESS_CHANCE}')
        print(f'Average berries across 10 iterations at this level: {format_with_commas(avg_gen)}')

        # compare this berry av to our best berry obtaining generation
        if avg_gen > most_berries:
            # if it is better, write that down!
            most_berries = avg_gen
            best_forgiveness = bnb.FORGIVENESS_CHANCE
            bpg = avg_bear
        
    return most_berries, bpg, best_forgiveness

def create_equal_generation(b: int):
    # b is the number of bears to create of each strat type 
    bears = bnb.create_bear_generation(b, b, b, b, b, b, b)
    return bears

def play_and_record_lifetime(num_seasons, num_strat):
    bears = create_equal_generation(num_strat)

    play_lifetime(num_seasons, bears)

    eff, ste, ran, wsls, wolf, eye, grim, gen = collect_data(bears, num_seasons, num_strat)
    print_results_overall(eff, ste, ran, wsls, wolf, eye, grim, gen)
    print_head_to_head_bpg(bears)

def main():
    seasons_in_a_lifetime = 5
    bears_of_each_strat = 25

    play_and_record_lifetime(seasons_in_a_lifetime, bears_of_each_strat)

    # gen_berries, bear_bpg, f = find_best_society(seasons_in_a_lifetime, bears_of_each_strat)
    # print(f'Ideal society: {f}% forgiveness yields {format_with_commas(gen_berries)} berries with {seasons_in_a_lifetime} seasons in a lifetime')
    # print(f'In this society, each bear averaged {bear_bpg:.2f} berries per game.')

if __name__ == "__main__":
    main()
