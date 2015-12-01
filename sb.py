import sys

class oneliner:
  """An options class for reading from file and command line"""
  def __init__(self):
    self.opts = {} # dictionary of 3-tuples for options
    self.helpmsg = '\n command line options expected: \n'
    
    
  # add options, one at a time
  def addopt(self, optname, optval, helptxt='', opttype=0):
    if opttype == 0:
      opttype = type(optval).__name__
    elif opttype == 'int':
      optval = int(optval)
    elif opttype == 'float':
      optval = float(optval)

    if optname in self.opts:
      if len(helptxt) == 0:
        helptxt = self.opts[optname][3]
      self.opts[optname] = [self.opts[optname][0], optval, opttype, helptxt]
    else:
      self.opts[optname] = [len(self.opts),optval, opttype, helptxt]


  # get option, if set
  def getopt(self, optname):
    if optname in self.opts:
      self.fixtype(optname)
      return self.opts[optname][1]
    else:
      return None


  # read all options from command line
  def parsecmd(self, argv):
    i=1
    while i < len(argv):
      key = argv[i].replace('-','')
      value = True
      if (key == 'h')  | (key == 'help'):
        self.addopt('help',True, helptxt='set to display a help message',opttype='bool')
        i +=1
        continue
      if i < len(argv)-1:
        if argv[i+1][0] != '-':
          value = argv[i+1]
          i += 1
 

      # if option was explicitly added (via addopt, say) overwrite value only 
      if key in self.opts:
        self.opts[key][1] = value
      # otherwise, use a default value and help string
      else:
        opttype = type(value).__name__
        # TODO best guess at ints and floats
        self.opts[key] = [len(self.opts),value, opttype, '<undeclared option>']
      i += 1

  # read all options from a file
  # 
  # file format:
  # 
  # - a line beginning with '>' lists the option name
  # - the line immediately following the option name has k option vals, to
  #   be read in as a list
  # - if more than one value, create an array 
  # - all other lines are ignored, but should use '#' to signify comment.
  #
  # example:
  # 
  # > <optname>
  # <optval1> <optval2> ... <optvalk>
  #
  def parsefile(self, fname):
    f=open(fname,'r')
     
    w=f.readline().replace(' ', '')
    while w != '':
      
      # TODO case insensitivity?
      if w[0] == '>':
        w=w.replace('\n','')
      
        key = w[1:]
        value = [True]
   
        w=f.readline()
        if (w.strip(' ')[0] != '>') & (w.strip(' ')[0] != '\n'):
          value = w.strip().replace('  ',' ').replace('  ',' ').split(' ')
          w=w.replace(' ','')
       
        if key in self.opts:
          if len(value) == 1:
            if self.opts[key][2] == 'int':
              self.opts[key][1] = int(value[0])
            if self.opts[key][2] == 'float':
              self.opts[key][1] = float(value[0])
            else: 
              self.opts[key][1] = value[0]
          else:
            self.opts[key][1] = value
        else:      
          opttype = type(value[0]).__name__
          # TODO best guess at ints and floats
          if len(value) == 1:
            self.opts[key] = [len(self.opts),value[0], opttype, '<undeclared option>']
          else:  
            self.opts[key] = [len(self.opts),value, opttype, '<undeclared option>']
 
      else:   
        w=f.readline().replace(' ','')

    f.close()
    

  def printopts(self):
    
    if 'help' in self.opts:
      if self.opts['help'][1]:
        print(self.helpmsg)

    oploop = self.opts.keys()
    strops = [['' for _ in range(4)] for _ in range(len(oploop))]    
    widths = [4,4,4,4]
    i = 0
    for op in oploop:
      if len(op) > widths[0]:
        widths[0] = len(op)
      if len(self.opts[op][1].__str__()) > widths[1]:
        widths[1] = len(self.opts[op][1].__str__())
      if len(self.opts[op][2].__str__())+2 > widths[2]:
        widths[2] = len(self.opts[op][2].__str__())+2
      if len(self.opts[op][3].__str__()) > widths[3]:
        widths[3] = len(self.opts[op][3].__str__())
      
      strops[self.opts[op][0]][0] = op
      strops[self.opts[op][0]][1] = self.opts[op][1].__str__()
      strops[self.opts[op][0]][2] = '<%s>' % self.opts[op][2].__str__() 
      strops[self.opts[op][0]][3] = self.opts[op][3].__str__()
      i += 1

    # TODO pretty print for long help texts?

    # TODO pretty print for long vectors?

    i = 0
    for op in oploop:
      print('  %s = %s %s  %s' % (strops[i][0].ljust(widths[0]), strops[i][1].ljust(widths[1]), strops[i][2].ljust(widths[2]), strops[i][3].ljust(widths[3]))  )
      i += 1 

    print('')


  def fixtype(self, optname):
    if optname in self.opts:
      if type(self.opts[optname][1]).__name__ == 'list':
        for i in range(len(self.opts[optname][1])):
          if self.opts[optname][2] == 'int':
            self.opts[optname][1][i] = int(self.opts[optname][1][i])
          elif self.opts[optname][2] == 'float':
            self.opts[optname][1][i] = float(self.opts[optname][1][i])
      else:
        if self.opts[optname][2] == 'int': 
          self.opts[optname][1] = int(self.opts[optname][1])
        if self.opts[optname][2] == 'float':
          self.opts[optname][1] = float(self.opts[optname][1])
# end class oneliner 

