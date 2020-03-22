# run script by typing the follwing in the shell
# topographica/topographica -i -p retina_density=25 -p lgn_density=25 -p cortex_density=99 topographica/examples/gcal_mod.ty
# topographica -i -p retina_density=25 -p lgn_density=25 -p cortex_density=99 miniconda3/envs/py4topo/share/topographica/examples/gcal_mod.ty

# topographica -a -c "run_batch('miniconda3/envs/py4topo/share/topographica/examples/gcal_mod.ty',retina_density=25,lgn_density=25,cortex_density=99)" \
# topographica -a -c "run_batch('miniconda3/envs/py4topo/share/topographica/examples/gcal_mod.ty',retina_density=61,lgn_density=61,cortex_density=245)" \
# -c "topo.sim.run(10000)"
# -c "save_snapshot()"

topo.sim.run(10000) #in the parenthesis is the number of learning iterations
# topo.command.load_snapshot('LOCATION/FILENAME')


id_nl = topo.sim['Retina'].sheet2matrixidx(-0.5, 0.5)  #north-left
id_nr = topo.sim['Retina'].sheet2matrixidx(0.5, 0.5)   #north-right
id_sl = topo.sim['Retina'].sheet2matrixidx(-0.5, -0.5) #south-left
idlist_x = range(id_nl[1], id_nr[1]+1) #north-left to north-right
idlist_y = range(id_nl[0], id_sl[0]+1) #north-left to south-left

import topo.pattern
pt_delta = topo.pattern.RawRectangle(xdensity=topo.sim['Retina'].density, ydensity=topo.sim['Retina'].density,bounds=topo.sim['Retina'].bounds, size=1/topo.sim['Retina'].density, scale=0.3)
pt_gauss = topo.pattern.Gaussian(xdensity=topo.sim['Retina'].density,ydensity=topo.sim['Retina'].density,bounds=topo.sim['Retina'].bounds,aspect_ratio=1, scale=0.3)
pt_gauss.size = 0.125
#MULTIPLY THE 'SIZE' variable with a constant to increase the size of the stimulus
pt_bg=topo.pattern.random.GaussianRandom(xdensity=topo.sim['Retina'].density,ydensity=topo.sim['Retina'].density,bounds=topo.sim['Retina'].bounds,scale=0.001,offset=0.5)
pt=topo.pattern.Composite(generators=[pt_bg,pt_gauss],xdensity=topo.sim['Retina'].density,ydensity=topo.sim['Retina'].density)
pt_pos = pt
pt_neg = pt
pt_pos.operator=numpy.add
pt_neg.operator=numpy.subtract


import topo.command, numpy

nx=id_nr[1]-id_nl[1]+1 #number of retinal array columns
ny=id_sl[0]-id_nl[0]+1 #number of retinal array rows
ncell_v1=numpy.prod(topo.sim['V1'].shape) #number of v1 cell array elements
output_pos=numpy.zeros((nx, ny, ncell_v1))    #for each retinal location (stimulus location), and for each V1 cell
output_neg=numpy.zeros((nx, ny, ncell_v1))    #for each retinal location (stimulus location), and for each V1 cell

for c in range(0,nx): 
   for r in range(0,ny):
      # generate stimulus for each retinal cell location
      this_pos = topo.sim['Retina'].matrixidx2sheet(idlist_y[r],idlist_x[c])
      #pt_delta.position = this_pos
      pt_gauss.position = this_pos
      # present the stimulus
      holder_arr_pos = numpy.zeros(topo.sim['V1'].shape)
      holder_arr_neg = numpy.zeros(topo.sim['V1'].shape)
      for iter in range(0,101):
        topo.command.pattern_present(inputs=pt_pos)
        holder_arr_pos = holder_arr_pos + topo.sim['V1'].activity
        topo.command.pattern_present(inputs=pt_neg)
        holder_arr_neg = holder_arr_neg + topo.sim['V1'].activity
        
      print("x: %f, y: %f" %(this_pos) + " {row %d(%d) col %d(%d))" %(r, idlist_y[r], c, idlist_x[c]))
      #output[r,c,:] = numpy.reshape(topo.sim['V1'].activity, (1,ncell_v1))
      output_pos[r,c,:] = numpy.reshape(holder_arr_pos, (1,ncell_v1))
      output_neg[r,c,:] = numpy.reshape(holder_arr_neg, (1,ncell_v1))
      #numpy.savetxt("Topographica/respV1_stim_row%d_col%d.csv"%(r,c), topo.sim['V1'].activity, delimiter=",")

import os
os.makedirs("Topographica/v1_rf_post")
for i in range(0,ncell_v1):
   i_r = i/topo.sim['V1'].shape[0]
   i_c = i%topo.sim['V1'].shape[0]
   print("Saving RF: ID=%d, row=%d, col=%d"%(i,i_r,i_c))
   numpy.savetxt("Topographica/v1_rf_post/v1_rf_cellid%04d_row%d_col%d_pos.csv"%(i,i_r,i_c), output_pos[:,:,i], delimiter=",")
   numpy.savetxt("Topographica/v1_rf_post/v1_rf_cellid%04d_row%d_col%d_neg.csv"%(i,i_r,i_c), output_neg[:,:,i], delimiter=",")

import topo.command.analysis
topo.command.analysis.save_plotgroup("Orientation Preference")