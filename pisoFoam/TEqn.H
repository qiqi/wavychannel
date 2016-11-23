// Solve the scalar equation
//
double Pr = 5.0;

fvScalarMatrix TEqn
(
    fvm::ddt(T) + fvm::div(phi, T)
  - fvm::laplacian(turbulence->nu() / Pr, T)
 ==
    fvOptions(T)
);

TEqn.relax();

fvOptions.constrain(TEqn);

TEqn.solve();

fvOptions.correct(T);
