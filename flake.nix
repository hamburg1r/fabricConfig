{
  description = "My Fabric Bar Test V1";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";

    fabric = {
      url = "github:nikitax44/fabric/run-widget_qol";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    fabric-libgray = {
      url = "github:Fabric-Development/gray";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    # fabric-libglace = {
    #   url = "github:Fabric-Development/glace/hyprland";
    #   inputs.nixpkgs.follows = "nixpkgs";
    # };
  };

  outputs = {
    self,
    nixpkgs,
    utils,
    fabric,
    ...
  } @ inputs:
    utils.lib.eachDefaultSystem (
      system: let
        overlays = [
          # (_: _: {fabric-libglace = inputs.fabric-libglace.packages.${system}.default;})
          # (_: _: {inherit (nixpkgs.legacyPackages.${system}) basedpyright;})
          (_: _: {fabric-libgray = inputs.fabric-libgray.packages.${system}.default;})
          #
          (_: _: {gengir = pkgs.python3Packages.callPackage ./nix/gengir.nix {};})
          # (_: _: {rlottie-python = pkgs.python3Packages.callPackage ./nix/rolttie-python.nix {};})
          # (_: _: {pywayland-custom = pkgs.python3Packages.callPackage ./nix/pywayland.nix {};})
          (_: _: {inherit (fabric.packages.${system}) run-widget;})

          fabric.overlays.${system}.default
        ];

        pkgs = import nixpkgs {
          inherit system;
          inherit overlays;
        };
      in {
        # formatter = pkgs.nixfmt-rfc-style;
        devShells.default = pkgs.callPackage ./shell.nix {
          inherit pkgs;
        };
        packages.default = pkgs.callPackage ./derivation.nix {
          inherit (pkgs) lib python3Packages;
        };
        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/start-desktop";
        };
      }
    );
}
