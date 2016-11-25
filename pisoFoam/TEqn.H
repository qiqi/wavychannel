// Solve the scalar equation
//
double Pr = 5.0;

fvScalarMatrix TEqn
(
    fvm::ddt(T) + fvm::div(phi, T)
  - 1./Pr * fvm::laplacian(turbulence->nu(), T)
 ==
    fvOptions(T)
);

TEqn.relax();

fvOptions.constrain(TEqn);

TEqn.solve();

fvOptions.correct(T);
