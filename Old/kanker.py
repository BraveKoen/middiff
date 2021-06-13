from datetime import date




def new_inter(ci_KDA, ci_week, ni_KDA, ni_week, ni_lenght_game):
    week = date.today().isocalendar()[1]

    if ci_week < ni_week:
        return True
    if ni_KDA < ci_KDA and ni_lenght_game > 1140 and ni_week == week:
        return True
    return False


print(new_inter(3, 35, 23, 35, 20300))