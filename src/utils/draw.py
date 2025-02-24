import graphviz
from src.game_config import *

def draw_net(config, genome, filename="network"):
    """Draw the NEAT neural network with a dark background and colors."""
    dot = graphviz.Digraph(format='png', graph_attr={
            'bgcolor': '#222222',
            'ranksep': '6',  # Vertical spacing between layers
        },directory='output')

    # Create subgraphs to organize nodes by layers
    with dot.subgraph() as input_layer:
        input_layer.attr(rank="same")
        for node in config.genome_config.input_keys:
            input_layer.node(str(node), f"🔵 {node}", shape="ellipse", style="filled", fillcolor="#0043d4", fontcolor="white", fontname="bold")

    with dot.subgraph() as output_layer:
        output_layer.attr(rank="same")
        for node in config.genome_config.output_keys:
            output_layer.node(str(node), f"🟢 {node}", shape="ellipse", style="filled", fillcolor="#00b900", fontcolor="white", fontname="bold")

    with dot.subgraph() as hidden_layer:
        hidden_layer.attr(rank="same")
        for node in genome.nodes:
            if node not in config.genome_config.input_keys and node not in config.genome_config.output_keys:
                hidden_layer.node(str(node), f"🟡 {node}", shape="ellipse", style="filled", fillcolor="#c75a00", fontcolor="white", fontname="bold")

    # Create colored connections and dynamic thickness based on weight
    for (input_node, output_node), conn in genome.connections.items():
        if conn.enabled:
            weight = conn.weight
            color = f"#{int(max(0, min(255, 255 - (weight * 100)))):02X}FF{int(max(0, min(255, 255 + (weight * 100)))):02X}"  # Red-green gradient
            penwidth = str(max(1, abs(weight * 3)))  # The greater the weight, the thicker the line
            dot.edge(str(input_node), str(output_node), label=f"{weight:.2f}", color=color, penwidth=penwidth, fontcolor="white", fontname="bold")
        else:
            # Disabled connections are displayed as dashed lines
            dot.edge(str(input_node), str(output_node), label=f"{conn.weight:.2f}", color="gray", style="dashed", fontcolor="white")

    # Save and render
    dot.render(filename, view=False)
    print(f"Network saved as {filename}.png")

def draw_info(font, num_dinos, game_speed, points, best_points, count_round, best_round, max_fitness):
    """Draw the score and AI information on the screen."""
    texts = [
        f"Generation: {count_round}",
        f"Dinos: {num_dinos}",
        f"Score: {points}",
        f"Best Gen: {best_round}",
        f"Best Score: {best_points}",
        f"Fitness: {max_fitness:.2f}",
        f"Speed: {game_speed}",
    ]
    
    y_offset = 20
    for text in texts:
        rendered_text = font.render(text, True, (0, 0, 0))
        SCREEN.blit(rendered_text, (900, y_offset))
        y_offset += 30  # Spacing between lines

def draw_sqr_dino(dino):
    """Draw a square representing the dino."""
    if dino.dino_jump:
        pygame.draw.rect(SCREEN, (255, 0, 0), dino.dino_rect, 2)
    elif dino.dino_run:
        pygame.draw.rect(SCREEN, (0, 0, 255), dino.dino_rect, 2)
    else:
        pygame.draw.rect(SCREEN, (0, 255, 0), dino.dino_rect, 2)


def draw_srq_obstacle(obstacle):
    """Draw a square representing the obstacle."""
    pygame.draw.rect(SCREEN, (255, 0, 0), obstacle.rect, 2)  # Draw a red rectangle around the obstacle

def draw_line(dino_position, obstacles):
    pygame.draw.line(SCREEN, (0, 255, 0),
                        (dino_position),
                        (obstacles[0].rect.x, obstacles[0].rect.y),
                        2) # This line represents the height of the obstacle
    pygame.draw.line(SCREEN, (0, 0, 255),
                        (dino_position),
                        (obstacles[0].rect.x + obstacles[0].rect.width, obstacles[0].rect.y + obstacles[0].rect.height // 2),
                        2) # This line represents the width of the obstacle
    pygame.draw.line(SCREEN, (255, 255, 0),
                        (dino_position),
                        (obstacles[0].rect.x, obstacles[0].rect.y + obstacles[0].rect.height),
                        2) # This line represents the lower height of the obstacle