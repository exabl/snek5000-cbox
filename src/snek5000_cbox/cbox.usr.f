!-----------------------------------------------------------------------
      subroutine uservp (ix,iy,iz,ieg)
      include 'SIZE'
      include 'NEKUSE'          
      include 'INPUT'           
      include 'TSTEP'           

      udiff = 0.
      utrans = 0.

      return
      end
!-----------------------------------------------------------------------
      subroutine userf  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'NEKUSE'          
      include 'PARALLEL'        
      include 'SOLN'            
      include 'INPUT'           

      integer ix, iy, iz, ieg, iel
      real rtmp, Pr_

      Pr_ = abs(UPARAM(1))

      ! local element number
      iel = GLLEL(ieg)
      
      FFX = 0
      FFY = 0
      FFZ = 0
      ! forcing, put boussinesq
      if (IFPERT) then
         ip = ix + NX1*(iy-1+NY1*(iz-1+NZ1*(iel-1)))
         rtmp = TP(ip,1,1)*Pr_
      else
         rtmp = T(ix,iy,iz,iel,1)*Pr_
      endif

      FFX = 0
      FFY = rtmp
      if (IF3D) FFZ = 0

      return
      end
!-----------------------------------------------------------------------
      subroutine userq  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'

      qvol   = 0.
      source = 0.

      return
      end
!-----------------------------------------------------------------------
      subroutine userchk

      include 'SIZE'            
      include 'INPUT'           
      include 'TSTEP'           
      include 'SOLN'            

      integer n, nit_pert, nit_hist
      
      common /SCRUZ/ vtmp(lx1*ly1*lz1*lelt,ldim),ttmp(lx1*ly1*lz1*lelt)
      real vtmp, ttmp

      nit_hist = UPARAM(10)
      nit_pert = UPARAM(9)

      if (ISTEP.eq.0) then
         TIME = 0
      ! start framework
         call frame_start
      endif

      ! monitor simulation
      call frame_monitor
      call chkpt_main
      ! finalise framework
      if (istep.eq.nsteps.or.lastep.eq.1) then
         call frame_end
      endif

      ! perturbation field
      if (IFPERT) then
         if (mod(ISTEP,nit_pert).eq.0) then
      ! write perturbation field
             call out_pert()
         endif
      endif

      ! history points
      if (mod(ISTEP,nit_hist).eq.0) then
         if (.not. ifpert) then
             call hpts()
         else

             call opcopy(vtmp(1,1),vtmp(1,2),vtmp(1,ndim),vx,vy,vz)
             n = NX1*NY1*NZ1*NELV
             call copy(ttmp,T,n)
             call opcopy(vx, vy, vz, vxp, vyp, vzp)
             call copy(T,TP,n)

             call hpts()

             call opcopy(vx,vy,vz, vtmp(1,1),vtmp(1,2),vtmp(1,ndim))
             call copy(T,ttmp,n)

         endif
      endif

      return
      end
!-----------------------------------------------------------------------
      subroutine userbc (ix,iy,iz,iside,ieg)
      include 'SIZE'
      include 'GEOM'            
      include 'INPUT'
      include 'SOLN'            
      include 'NEKUSE'
      
      integer ntot
      real delta_T_side, delta_T_vert, aspect_ratio
      real xmax, ymax, dTl, dTv

      delta_T_side = UPARAM(5)
      delta_T_vert = UPARAM(6)
      aspect_ratio = UPARAM(8)
        
      ymax = 1.
      xmax = ymax/aspect_ratio

      dTl = delta_T_side/2.
      dTv = delta_T_vert/2.

      ! base flow
      if (JP.eq.0) then
         ux = 0.
         uy = 0.
         uz = 0.

         if (delta_T_side.ne.0.and.delta_T_vert.eq.0) then      
             if (x.eq.0) then
               temp = -dTl
             elseif (x.eq.xmax) then
                 temp = dTl
             endif

         elseif (delta_T_vert.ne.0.and.delta_T_side.eq.0) then      
             if (y.eq.0) then
                 temp = dTv
             elseif (y.eq.ymax) then   
                 temp = -dTv
             endif
      
         elseif (delta_T_side.ne.0.and.delta_T_vert.ne.0) then
             if (x.eq.0) then
                 temp = -dTl
             elseif (x.eq.xmax) then
                 temp = dTl     
             elseif(y.eq.0) then
                 temp = dTv
             elseif (y.eq.ymax) then
                 temp = -dTv
             elseif (x.eq.0.and.y.eq.0) then
                 temp = (dTv-dTl)/2.
             elseif (x.eq.0.and.y.eq.ymax) then
                 temp = (-dTv-dTl)/2.
             elseif (x.eq.xmax.and.y.eq.0) then
                 temp = (dTl+dTv)/2.        
             elseif (x.eq.xmax.and.y.eq.ymax) then
                 temp = (dTl-dTv)/2.        
             endif
         endif

      ! perturbation
      else
         ux = 0.
         uy = 0.
         uz = 0.
         temp = 0.
      endif

      return
      end
!-----------------------------------------------------------------------
      subroutine useric (ix,iy,iz,ieg)
      include 'SIZE'
      include 'NEKUSE'
      include 'SOLN'            
      include 'GEOM'            
      include 'INPUT'

      real delta_T_side, delta_T_vert, amplitude, aspect_ratio
      real xmax, ymax, ran

      delta_T_side = UPARAM(5)
      delta_T_vert = UPARAM(6)
      amplitude = UPARAM(7)
      aspect_ratio = UPARAM(8)
        
      ymax = 1.
      xmax = ymax/aspect_ratio

      ! base flow
      if (JP.eq.0) then
    
         ux = 0.0
         uy = 0.0
         uz = 0.0
         
         call random_number(temp)
         temp = amplitude * temp

         if (delta_T_vert.ne.0.and.delta_T_side.eq.0) then
             temp = delta_T_vert * (0.5- y/ymax) + temp 
         elseif (delta_T_side.ne.0.and.delta_T_vert.eq.0) then
             temp = -delta_T_side * (x/xmax - 0.5) + temp
         endif
         
      ! perturbation
      else

         ux = 0.0
         uy = 0.0 
         uz = 0.0

         call random_number(temp)
         temp = amplitude * temp
      endif

      return
      end
!-----------------------------------------------------------------------
      ! This routine to modify element vertices
      subroutine usrdat
      include 'SIZE'

      return
      end
!-----------------------------------------------------------------------
      subroutine usrdat2
      include 'SIZE'
      include 'GEOM'           
      include 'INPUT'           
      include 'SOLN'

      integer i, ntot
      real stretch_x, stretch_y, stretch_z, xx, yy, zz, twopi
      real xmax, ymax, zmax

      stretch_x = UPARAM(4)

      if (stretch_x.ne.0.0) then
         ntot = nx1*ny1*nz1*nelt

         xmax = glmax(xm1,ntot)
         ymax = glmax(ym1,ntot)
         if (if3d) then
             zmax = glmax(zm1,ntot)
         endif

         twopi = 8 * atan(1.)

      ! stretch factors
         stretch_y = stretch_x*ymax
         if (if3d) then
             stretch_z = stretch_x*zmax
         endif   
            
         do i=1,ntot
             xx = xm1(i,1,1,1)
             yy = ym1(i,1,1,1)
             xm1(i,1,1,1) = xx - (stretch_x * (sin(twopi*xx/xmax)))
             ym1(i,1,1,1) = yy - (stretch_y * (sin(twopi*yy/ymax)))
            
             if (if3d) then
                 zz = zm1(i,1,1,1)
                 zm1(i,1,1,1) = zz - (stretch_z * (sin(twopi*zz/zmax)))
             endif   
         enddo
      endif      
      
      return
      end
!-----------------------------------------------------------------------
      subroutine usrdat3

      return
      end
!-----------------------------------------------------------------------
      subroutine frame_usr_register
      implicit none
      include 'SIZE'
      include 'FRAMELP'

      ! register modules
      call io_register
      call chkpt_register

      return
      end subroutine
!-----------------------------------------------------------------------
      subroutine frame_usr_init
      implicit none
      include 'SIZE'
      include 'FRAMELP'

      ! initialise modules
      call chkpt_init

      return
      end subroutine
!-----------------------------------------------------------------------
      subroutine frame_usr_end
      implicit none
      include 'SIZE'
      include 'FRAMELP'
      
      return
      end subroutine
