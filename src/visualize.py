import plotly.express as px
import pandas as pd

def add_cur_hospital_info(data, instance,  hospital_infos, cur_time):
    for hlist in hospital_infos:
        h = instance.hospitals[hlist[0]]
        data.append([cur_time, h.ident, h.position.lat, h.position.lon, 100 - hlist[1]])


def hospital_visualization(instance, start, end, ticks):

    time_steps = sorted([t for t in instance.snapshots])
    data_list = []

    i = 0
    for t in range(ticks):

        cur_time = round(start + t / ticks * (end - start))

        while i + 1 < len(time_steps) and time_steps[i + 1] <= cur_time:
            i += 1
        add_cur_hospital_info(data_list, instance, instance.snapshots[time_steps[i]], cur_time)

    df = pd.DataFrame(data_list, columns = ['time', 'id', 'y', 'x', 'capacity_score'])

    fig = px.scatter(df, x = 'x', y = 'y', animation_frame= 'time', animation_group = 'id', color = 'capacity_score', color_continuous_scale=[(0.00, "green"),   (0.33, "yellow"),
                                                     (0.66, "red"), (1.0, "black")], hover_name = 'id', range_x = [8, 12], range_y = [48, 52], width=800, height=1200)
    fig.add_layout_image(dict(source="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Karte_Deutschland.svg/1000px-Karte_Deutschland.svg.png"),
            xref="x",
            yref="y",
            x=8,
            y=52,
            sizex=4,
            sizey=4,
            sizing="stretch",
            opacity=0.5,
            layer="below")
    #fig.update_traces(marker=dict(size = 20))
    #fig.show()
    html_dump = fig.to_html()
    with open("data/visualization/hospitals.html", "w") as f:
        f.write(html_dump)

def corona_visualization(instance, start, end, ticks):

    # TODO: visible for more time steps
    nbr_ticks_visible = 10

    reqs = sorted(instance.requests.values(), key = lambda r : r.filed_at)

    data_list = []
    times = [round(start + t / ticks * (end - start)) for t in range(ticks)]

    r_id = 0
    for t in range(ticks):

        cur_time = times[t]

        while r_id + 1 < len(reqs) and reqs[r_id + 1].filed_at <= cur_time:
            r = instance.requests[str(r_id)]
            for i in range(nbr_ticks_visible):
                if i + t >= ticks:
                    break
                data_list.append([times[i + t], r.ident, r.person.position.lon, r.person.position.lat])
            r_id += 1
    df = pd.DataFrame(data_list, columns = ['time', 'id', 'x', 'y'])


    fig = px.scatter(df, x = 'x', y = 'y', animation_frame= 'time', animation_group = 'id', hover_name = 'id', range_x = [8, 12], range_y = [48, 52], width=800, height=1200)
    fig.add_layout_image(dict(source="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Karte_Deutschland.svg/1000px-Karte_Deutschland.svg.png"),
            xref="x",
            yref="y",
            x=8,
            y=52,
            sizex=4,
            sizey=4,
            sizing="stretch",
            opacity=0.5,
            layer="below")
    #fig.show()
    html_dump = fig.to_html()
    with open("data/visualization/patients.html", "w") as f:
        f.write(html_dump)


def visualize(instance):
    time_frame_start = min(r.filed_at for r in instance.requests.values())
    time_frame_end = max(r.filed_at for r in instance.requests.values())
    nbr_ticks = 100

    # okay, lets go
    hospital_visualization(instance, time_frame_start, time_frame_end, nbr_ticks)
    corona_visualization(instance, time_frame_start, time_frame_end, nbr_ticks)
