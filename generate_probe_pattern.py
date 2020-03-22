from topo import pattern
%% https://ioam.github.io/topographica/User_Manual/patterns.html

#Each pixel is chosen independently from a Gaussian distribution
#of zero mean and unit variance, then multiplied by the given
#scale and adjusted by the given offset.

input_type=pattern.GaussianRandom
#    total_num_inputs=int(p.num_inputs*p.area*p.area)
#    inputs=[input_type(x=numbergen.UniformRandom(lbound=-(p.area/2.0+0.25),
#                                                 ubound= (p.area/2.0+0.25),seed=12+i),
#                       y=numbergen.UniformRandom(lbound=-(p.area/2.0+0.25),
#                                                 ubound= (p.area/2.0+0.25),seed=35+i),
#                       orientation=numbergen.UniformRandom(lbound=-pi,ubound=pi,seed=21+i),
#                       size=0.088388, aspect_ratio=4.66667, scale=p.scale)
#            for i in xrange(total_num_inputs)]
#
#    combined_inputs = pattern.SeparatedComposite(min_separation=0,generators=inputs)
#
#elif p.dataset=="Nature":

#var = pattern
#numpyarray = pattern()


#pt_delta=pattern.RawRectangle(xdensity=topo.sim['Retina'].density, ydensity=topo.sim['Retina'].density, size=1/topo.sim['Retina'].density, bounds=topo.sim['Retina'].bounds)
pt_delta=pattern.RawRectangle(xdensity=25, ydensity=25, size=1/25,scale=0.3)
pt_bg=pattern.random.GaussianRandom(xdensity=25,ydensity=25,scale=0.001,offset=0.5)
pt = pattern.Composite(generators=[pt_delta,pt_bg],operator=numpy.add,xdensity=25,ydensity=25)

numpy.histogram(pt())
topo.command.pattern_present(inputs=pt)
numpy.histogram(topo.sim['V1'].activity)

im_to_save = Image.fromarray(pt()*255)
im_to_save.convert('RGB').save('/mnt/c/Users/jiboonne/Documents/teststim.png', "PNG", optimize=True)

imagename = '/mnt/c/Users/jiboonne/Documents/image823.png'