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
         if (IFPERT) then
            call perturb_fields(ix,iy,iz,ieg)
         endif

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
      include 'TSTEP'
      include 'INPUT'
      include 'NEKUSE'
      common /rayleigh_r/ rapr,ta2pr

      ux=0.
      uy=0.
      uz=0.

      if (x.eq.0) then
         temp=-0.5000
      elseif (x .eq. 1.0) then
         temp=0.5000
      endif

      return
      end
!-----------------------------------------------------------------------
      subroutine useric (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'

      temp = 0
      ux=0.0
      uy=0.0
      uz=0.0

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
      real sfx, sfy, sfz, xx, yy, zz,twopi
      real xmax, ymax, zmax

      sfx = UPARAM(4)

      if (sfx .NE. 0.0) then
         ntot = nx1*ny1*nz1*nelt

         xmax = glmax(xm1,ntot)
         ymax = glmax(ym1,ntot)
         if (if3d) then
            zmax = glmax(zm1,ntot)
         endif

         twopi=8*atan(1.)

         !stretch factors
         sfy = sfx*ymax
         if (if3d) then
            sfz = sfx*zmax
         endif   
            
         do i=1,ntot
            xx = xm1(i,1,1,1)
            yy = ym1(i,1,1,1)
            xm1(i,1,1,1) = xx - (sfx * (sin(twopi*xx/xmax)))
            ym1(i,1,1,1) = yy - (sfy * (sin(twopi*yy/ymax)))
            
            if (if3d) then
                  zz = zm1(i,1,1,1)
                  zm1(i,1,1,1) = zz - (sfz * (sin(twopi*zz/zmax)))
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
      subroutine perturb_fields (ix,iy,iz,ieg)

      include 'SIZE'
      include 'NEKUSE'          ! UX, UY, UZ, TEMP, Z
      include 'SOLN'            ! V[XYZ], T, V[XYZ]P, TP, PRP

      ! velocity random distribution

      call random_number(VXP)
      VXP  = 0.00000001*(2*VXP - 1)

      call random_number(VYP)
      VYP  = 0.00000001*(4*VYP - 2)

      UZP = 0.0

      ! temperature random distribution
      call random_number(TP)
      TP= 0.00000001*(TP - 0.5)

      ! pressure random distribution
      !call random_number(PRP)
      !PRP= 0.000001*(0.5*PRP - 0.25)

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
