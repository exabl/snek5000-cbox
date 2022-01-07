!-----------------------------------------------------------------------
      subroutine uservp (ix,iy,iz,ieg)
      include 'SIZE'
      include 'NEKUSE'          ! UDIFF, UTRANS
      include 'INPUT'           ! UPARAM
      include 'TSTEP'           ! TSTEP

      ! argument list
      integer ix, iy, iz, ieg

      ! local variables
      real Pr_,Ra_

      ! decide the non dimensionalization of the equations
      Pr_ = abs(UPARAM(1))
      Ra_ = abs(UPARAM(2))
      ! set the coefficients
      ! direct problem

      if (IFIELD.eq.1) then     !     momentum equations
            UTRANS = 1./Pr_
            UDIFF  = 1./sqrt(Ra_)
      elseif (IFIELD.eq.2) then !     temperature equation
            UTRANS = 1.0
            UDIFF  = 1./sqrt(Ra_)
      endif

      return
      end
!-----------------------------------------------------------------------
      subroutine userf  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'NEKUSE'          ! FF[XYZ]
      include 'PARALLEL'        ! GLLEL
      include 'SOLN'            ! VTRANS,TP
      include 'INPUT'           ! IF3D
      include 'ADJOINT'         ! IFADJ, G_ADJ

      ! argument list
      integer ix,iy,iz,ieg

      ! local variable
      integer iel
      real rtmp

      ! local element number
      iel=GLLEL(ieg)

      ! forcing, put boussinesq
      if (IFPERT) then
      ip=ix+NX1*(iy-1+NY1*(iz-1+NZ1*(iel-1)))
      rtmp = TP(ip,1,1)/VTRANS(ix,iy,iz,iel,1)
      else
      rtmp = T(ix,iy,iz,iel,1)/VTRANS(ix,iy,iz,iel,1)
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

      qvol   = 0.0
      source = 0.0

      return
      end
!-----------------------------------------------------------------------
      subroutine userchk

      include 'SIZE'            ! NX1, NY1, NZ1, NELV, NIO
      include 'INPUT'           ! UPARAM, CPFLD
      include 'TSTEP'           ! ISTEP, IOSTEP, TIME, LASTEP
      include 'SOLN'            ! V[XYZ], T, V[XYZ]P, TP, PRP
      include 'MASS'            ! BM1
      include 'ADJOINT'         ! IFADJ, G_ADJ, BETA_B, DTD[XYZ]

      ! local variables

      integer n, nit_pert, nit_hist
      real Pr_,Ra_

      nit_hist = UPARAM(10)
      nit_pert = UPARAM(3)

      if (ISTEP.eq.0) then
            TIME = 0
!     start framework
            call frame_start

      ! decide the non dimensionalization of the equations
            Pr_ = abs(UPARAM(1))
            Ra_ = abs(UPARAM(2))

      ! set fluid properties
            if (IFADJ) then
            CPFLD(1,1)=Pr_/sqrt(Ra_)
            CPFLD(1,2)=1.0

            CPFLD(2,1)=1.0/sqrt(Ra_)
            CPFLD(2,2)=1.0
            else
            CPFLD(1,1)=1.0/sqrt(Ra_)
            CPFLD(1,2)=1.0/Pr_

            CPFLD(2,1)=1.0/sqrt(Ra_)
            CPFLD(2,2)=1.0
            endif
      endif

!     monitor simulation
      call frame_monitor
!     save/load files for full-restart
      call chkpt_main
!     finalise framework
      if (istep.eq.nsteps.or.lastep.eq.1) then
            call frame_end
      endif

      ! perturbation field
      if (IFPERT) then
            if (mod(ISTEP,nit_pert).eq.0) then
      !       write perturbation field
            call outpost2(VXP,VYP,VZP,PRP,TP,1,'prt')
            endif
      endif

      ! history points
      if (mod(ISTEP,nit_hist).eq.0) then
            call hpts()
      endif

      return
      end
!-----------------------------------------------------------------------
      subroutine userbc (ix,iy,iz,iside,ieg)
      include 'SIZE'
      include 'NEKUSE'
      include 'SOLN'            ! JP
      
      if (JP.eq.0) then
!     base flow
            ux=0.0
            uy=0.0
            if (if3d) then
            uz=0.0
            endif
            if (x.eq.0) then
            temp=-0.5000
            elseif (x.eq.1.0) then
            temp=0.5000           
            endif
      else
!     perturbation
            ux=0.0
            uy=0.0
            if (if3d) then
            uz=0.0
            endif
            temp=0.0
      endif
      
      return
      end
!-----------------------------------------------------------------------
      subroutine useric (ix,iy,iz,ieg)
      include 'SIZE'
      include 'NEKUSE'
      include 'SOLN'            ! JP
      include 'INPUT'

!     argument list
      integer ix,iy,iz,ieg
      real amp, ran

      if (JP.eq.0) then
            ux=0.0
            uy=0.0
            uz=0.0
            temp=0
      else
!     perturbation; white noise

      rand = 2.e4*(ieg+x*sin(y)) + 1.e3*ix*iy + 1.e5*ix 
      rand = 1.e3*sin(rand)
      rand = 1.e3*sin(rand)
      rand = cos(rand)
      amp = .01

      ux   = amp*rand*sin(x)*cos(y)
      ux   = amp*(2*ux - 1)
      uy   = amp*rand*-cos(x)*sin(y)
      uy   = amp*(4*uy - 2)
      uz   = amp*rand*-cos(x)*cos(y)

      temp = amp*rand*cos(x)*cos(y)
      temp   = amp*(temp - 0.5)
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
      include 'GEOM'            ! {x,y,z}m1
      include 'INPUT'           ! param
      include 'SOLN'

      integer i, ntot
      real stretch_x, stretch_y, stretch_z, xx, yy, zz, twopi
      real xmax, ymax, zmax

      stretch_x = UPARAM(4)

      if (stretch_x .NE. 0.0) then
            ntot = nx1*ny1*nz1*nelt

            xmax = glmax(xm1,ntot)
            ymax = glmax(ym1,ntot)
            if (if3d) then
            zmax = glmax(zm1,ntot)
            endif

            twopi=8*atan(1.)

            !stretch factors
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

!     register modules
      call io_register
      call chkpt_register

      return
      end subroutine
!-----------------------------------------------------------------------
      subroutine frame_usr_init
      implicit none
      include 'SIZE'
      include 'FRAMELP'

!     initialise modules
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
!-----------------------------------------------------------------------

      
      