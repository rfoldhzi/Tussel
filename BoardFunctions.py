
import GlobalVaribles as GV

def highlightSquare(x,y):
    rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
    GV.pygame.draw.rect(GV.DISPLAYSURF, (255,255,255), rect)