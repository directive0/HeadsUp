#! /usr/bin/env python

"""

    I shamelessly stole this from here:
    
    Original Author: David Clark (da_clark at shaw.ca)

    http://www.pygame.org/pcr/text_rect/index.php
    
    It has been modified to suit my needs.
    
"""

class TextRectException():
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class TextBlock(object):
    

    def render_textrect(self,string, font, rect, text_color, background_color, pagenum, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.
    
        Takes the following arguments:
    
        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
                     text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified
        
        Pagenum - Desired area of text to display.
    
        Returns the following values:
    
        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """
    
        import pygame
        
        final_lines = []
    
        requested_lines = string.splitlines()
    
        # Create a series of lines that will fit on the provided
        # rectangle.
    
        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise TextRectException
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.    
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line 
                    else: 
                        final_lines.append(accumulated_line) 
                        accumulated_line = word + " " 
                final_lines.append(accumulated_line)
            else: 
                final_lines.append(requested_line) 
    
        # Let's try to write the text out on the surface.
        
        
        # first we know that at our text height we can only accomodate 14 lines, so we need to ensure we can capture only the right amount of text so we don't throw an exception
    
        surface = pygame.Surface(rect.size) 
        surface.fill(background_color) 
        accumulated_height = 0
       
        # make a list to hold our working strings.
        working_lines = []
        
    
        page = (pagenum * 14)
    
        nolines = len(final_lines)
        
        # the following dealy splits the strings up into groups of 15 so we can view them as pages. The variable "pagenum" lets us know where we are.

        if len(final_lines) > 14:
            for i in range(14):
                target = page + (i)

                if target >= len(final_lines):
                    pass
                else:
                    working_lines.append(final_lines[target])
        
            final_lines = working_lines
        
        for line in final_lines: 
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise TextRectException
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException
            accumulated_height += font.size(line)[1]
    
        return surface
    
